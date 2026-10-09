"""Publish a pinned, accepted Ubuntu package; never replace published assets."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tarfile
import tempfile
import time
import urllib.error
import urllib.request
import zipfile


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
    root = Path('releases/v0.3.0')
    manifest = json.loads((root / 'manifest.json').read_text())
    repo = os.environ['GITHUB_REPOSITORY']
    assert repo == 'maganrobotics-boop/OmindOS-Manipulation-Release' == manifest['destination']
    assert manifest['tag'] == 'v0.3.0'
    notes = (root / 'RELEASE_NOTES.zh-CN.md').read_text()
    accepted = json.loads((root / 'RELEASE_ACCEPTANCE.json').read_text())
    assert accepted['status'] == 'passed' and accepted['browser']['compiled_executable']
    assert accepted['source_commit'] == manifest['source_commit']
    try:
        prior = api('repos/' + repo + '/releases/tags/' + manifest['tag'])
    except urllib.error.HTTPError as error:
        if error.code != 404:
            raise
    else:
        if not prior['draft']:
            assert prior['name'] == manifest['title'] and prior['body'] == notes
            assert not prior['prerelease']
            check_assets(prior['assets'], manifest['assets'])
            print(json.dumps({'published': prior['html_url'], 'verified_assets': len(prior['assets'])}), flush=True)
            return
    with tempfile.TemporaryDirectory(prefix='omindos-accepted-') as temporary:
        output = Path(temporary)
        archive_zip = output / 'workflow.zip'
        assert manifest['download_url'].startswith('https://sdmnt')
        assert '.oaiusercontent.com/files/' in manifest['download_url']
        subprocess.run(['curl', '--fail', '--location', '--silent', '--show-error',
            '--user-agent', 'Mozilla/5.0', '--max-time', '120', '--proto', '=https',
            '--output', str(archive_zip), manifest['download_url']], check=True)
        assert digest(archive_zip) == manifest['workflow_archive_digest']
        with zipfile.ZipFile(archive_zip) as handle:
            assert all(Path(n).name == n for n in handle.namelist())
            handle.extractall(output)
        archive = output / 'omindos-workbench-0.3.0-linux-x64.tar.gz'
        archive_asset = next(a for a in manifest['assets'] if a['name'] == archive.name)
        assert (archive.stat().st_size, digest(archive)) == (archive_asset['size'], archive_asset['digest'])
        with tarfile.open(archive) as handle:
            prefix = 'omindos-workbench-0.3.0-linux-x64/'
            data = json.load(handle.extractfile(prefix + 'MANIFEST.json'))
            validation = json.load(handle.extractfile(prefix + 'VALIDATION.json'))
            assert data['source_commit'] == manifest['source_commit']
            assert data['version'] == '0.3.0' and not data['backend_source_included']
            assert data['planning_kernel_sha256'] == '1d59d526a76e6c76576bba4974fdbd9373820146f8ab2adff7893790e74cbef0'
            assert data['coupled_waist_dual_arm_planning'] and not data['dynamics_simulation_bundled']
            assert data['navigation_integrated'] and data['navigation_drive_types'] == ['differential','omnidirectional']
            assert data['navigation_kernel_sha256'] == 'f2922dec474d54625051f9d384a6d22f72e4795934995db3753b02f85ddac407'
            assert data['navigation_localization_source'] == 'geometric_simulator'
            assert accepted['navigation']['status'] == 'passed' and not accepted['navigation']['source_mode']
            assert validation['status'] == 'PASS' and validation['compiled_executable']
            for name, sha in data['files'].items():
                assert Path(name).suffix.lower() not in ('.py', '.pyc', '.pyo', '.pyz', '.c', '.cpp', '.h', '.map')
                assert hashlib.sha256(handle.extractfile(prefix + name).read()).hexdigest() == sha, name
        paths = []
        for asset in manifest['assets']:
            name = asset['name']
            assert Path(name).name == name
            path = output / name if asset['origin'] == 'artifact' else root / name
            assert (path.stat().st_size, digest(path)) == (asset['size'], asset['digest']), name
            paths.append(path)
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
            if all(a.get('digest') for a in release['assets']):
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
