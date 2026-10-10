"""Publish the accepted 0.3.1 Ubuntu package without replacing released assets."""
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import subprocess
import tarfile
import tempfile
import time
import urllib.error
import urllib.request


def api(path, payload=None, method=None):
    request = urllib.request.Request('https://api.github.com/' + path,
        data=None if payload is None else json.dumps(payload).encode(),
        headers={'Authorization': 'Bearer ' + os.environ['GH_TOKEN'],
                 'Accept': 'application/vnd.github+json', 'Content-Type': 'application/json',
                 'X-GitHub-Api-Version': '2022-11-28'}, method=method)
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.load(response)


def digest(path):
    hasher = hashlib.sha256()
    with path.open('rb') as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b''):
            hasher.update(block)
    return 'sha256:' + hasher.hexdigest()


def check_assets(actual, expected, complete=True):
    found = {a['name']: (a['size'], a.get('digest')) for a in actual}
    want = {a['name']: (a['size'], a['digest']) for a in expected}
    assert len(found) == len(actual) and set(found) <= set(want), 'Unexpected assets'
    assert all(want[n] == v for n, v in found.items()), 'Asset differs'
    if complete:
        assert found == want, 'Missing asset'


def main():
    root = Path('releases/v0.3.1')
    manifest = json.loads((root / 'manifest.json').read_text())
    repo = os.environ['GITHUB_REPOSITORY']
    assert repo == 'maganrobotics-boop/OmindOS-Manipulation-Release' == manifest['destination']
    assert manifest['tag'] == 'v0.3.1'
    assert manifest['source_commit'] == 'fdb6813a3d1877be7965a182022cbb1e5c7acb96'
    assert manifest['merged_source_commit'] == '0776da5d173ceab76c93648d4871dc6a3424a581'
    notes = (root / 'RELEASE_NOTES.zh-CN.md').read_text()
    accepted = json.loads((root / 'RELEASE_ACCEPTANCE.json').read_text())
    assert accepted['status'] == 'passed' and accepted['source_commit'] == manifest['source_commit']
    promotion = accepted['promotion']
    assert promotion['status'] == 'passed' and promotion['version'] == '0.3.1'
    assert promotion['changed_internal_files'] == ['MANIFEST.json']
    assert promotion['unchanged_internal_file_count'] == 201
    assert promotion['internal_hashes_verified'] and promotion['fresh_unpack_verify']
    assert promotion['fresh_unpack_startup_version'] == '0.3.1'
    assert accepted['full_CAD_installed_browser']['check_count'] == 9
    assert accepted['full_CAD_installed_browser']['status'] == 'passed'
    reports = accepted['independent_install']
    checks = [v for v in reports.values() if 'checks' in v]
    assert sum(len(v['checks']) for v in checks) == 46
    assert all(v['status'].lower() in ('pass', 'passed') for v in checks)
    with tempfile.TemporaryDirectory(prefix='omindos-accepted-031-') as temporary:
        output = Path(temporary)
        archive = output / 'omindos-workbench-0.3.1-linux-x64.tar.gz'
        assert manifest['download_url'] == ('https://omindos.cn/downloads/navigation/'
            'mda1-v0.3.1-0776da5d/' + archive.name)
        subprocess.run(['curl', '--fail', '--location', '--silent', '--show-error',
            '--retry', '2', '--max-time', '300', '--proto', '=https', '--proto-redir', '=https',
            '--output', str(archive), manifest['download_url']], check=True)
        archive_asset = next(a for a in manifest['assets'] if a['name'] == archive.name)
        assert (archive.stat().st_size, digest(archive)) == (archive_asset['size'], archive_asset['digest'])
        assert archive_asset['digest'] == 'sha256:' + promotion['sha256']
        with tarfile.open(archive) as handle:
            prefix = 'omindos-workbench-0.3.1-linux-x64'
            members = handle.getmembers()
            assert len({m.name for m in members}) == len(members), 'Duplicate tar members'
            for member in members:
                parts = PurePosixPath(member.name).parts
                assert parts and parts[0] == prefix and '..' not in parts
                assert member.isfile() or member.isdir(), 'Unexpected tar member type'
            data = json.load(handle.extractfile(prefix + '/MANIFEST.json'))
            validation = json.load(handle.extractfile(prefix + '/VALIDATION.json'))
            assert data['version'] == '0.3.1' and not data['backend_source_included']
            assert data['source_commit'] == manifest['source_commit']
            assert data['merged_source_commit'] == manifest['merged_source_commit']
            assert data['accepted_candidate_sha256'] == promotion['accepted_candidate_sha256']
            assert data['customer_cad_bundle']['manifest_sha256'] == promotion['model_manifest_sha256']
            assert data['customer_cad_bundle']['model_ids'] == ['6f', '6fb', 'b']
            assert data['customer_cad_bundle']['mesh_count'] == 14
            assert data['coupled_waist_dual_arm_planning'] and data['navigation_integrated']
            assert not data['dynamics_simulation_bundled'] and not data['hardware_validated']
            assert validation['status'] == 'PASS' and validation['compiled_executable']
            actual_files = {m.name[len(prefix) + 1:] for m in members if m.isfile()}
            assert actual_files == set(data['files']) | {'MANIFEST.json', 'VALIDATION.json'}
            for name, sha in data['files'].items():
                assert PurePosixPath(name).suffix.lower() not in ('.py', '.pyc', '.pyo', '.pyz', '.c', '.cpp', '.h', '.map')
                assert hashlib.sha256(handle.extractfile(prefix + '/' + name).read()).hexdigest() == sha, name
        paths = []
        for asset in manifest['assets']:
            name = asset['name']
            assert Path(name).name == name and asset['origin'] in ('artifact', 'repository')
            path = output / name if asset['origin'] == 'artifact' else root / name
            assert (path.stat().st_size, digest(path)) == (asset['size'], asset['digest']), name
            paths.append(path)
        if os.environ.get('VALIDATE_ONLY') == '1':
            print(json.dumps({'status': 'validated', 'assets': len(paths)}), flush=True)
            return
        endpoint = 'repos/' + repo + '/releases/tags/' + manifest['tag']
        try:
            release = api(endpoint)
        except urllib.error.HTTPError as error:
            if error.code != 404:
                raise
            release = api('repos/' + repo + '/releases', {
                'tag_name': manifest['tag'], 'target_commitish': os.environ['GITHUB_SHA'],
                'name': manifest['title'], 'body': notes, 'draft': True,
                'prerelease': False, 'make_latest': 'true'})
        assert release['name'] == manifest['title'] and release['body'] == notes
        assert not release['prerelease']
        check_assets(release['assets'], manifest['assets'], complete=not release['draft'])
        existing = {a['name'] for a in release['assets']}
        missing = [str(p) for p in paths if p.name not in existing]
        if missing:
            assert release['draft'], 'Do not modify a published release'
            subprocess.run(['gh', 'release', 'upload', manifest['tag'], '--repo', repo, *missing], check=True)
        endpoint = 'repos/' + repo + '/releases/' + str(release['id'])
        for attempt in range(20):
            release = api(endpoint)
            if len(release['assets']) == len(paths) and all(a.get('digest') for a in release['assets']):
                break
            time.sleep(3)
        check_assets(release['assets'], manifest['assets'])
        if release['draft']:
            api(endpoint, {'draft': False, 'prerelease': False, 'make_latest': 'true'}, 'PATCH')
        published = api(endpoint)
        assert not published['draft'] and not published['prerelease']
        check_assets(published['assets'], manifest['assets'])
        print(json.dumps({'published': published['html_url'], 'verified_assets': len(paths)}), flush=True)


if __name__ == '__main__':
    main()
