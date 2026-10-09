#!/usr/bin/env python3
"""Customer-side HTTP example; uses Python standard library only."""
import argparse
import json
import time
import urllib.request


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', default='http://127.0.0.1:8085')
    parser.add_argument('--drive', choices=('differential', 'omnidirectional'), default='differential')
    args = parser.parse_args()

    def request(path, payload=None):
        data = None if payload is None else json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(args.url.rstrip('/') + path, data=data,
                                     headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req, timeout=15) as response:
            return json.load(response)

    # Reference robot only. Replace profile/start/mapping/goal for customer hardware.
    profile = request('/example.json')
    config = request('/v1/navigation-config')['config']
    mapping = request('/v1/planning-config')['mapping']
    config['drive_type'] = args.drive
    start = {'waist_pitch': 0}
    for side, angles in [('left', [1.57, 1.3, -1.57, 1.1, .1, .5, 0]),
                         ('right', [-1.57, 1.3, 1.57, 1.1, -.1, .5, 0])]:
        start.update({f'{side}_joint_{i+1}': angle for i, angle in enumerate(angles)})
    task = request('/v1/navigation-start', {
        'profile': profile, 'start': start, 'mapping': mapping, 'config': config,
        'base_pose': {'x_m': 0, 'y_m': 0, 'yaw_rad': 0},
        'goal': {'x_m': .12, 'y_m': .1, 'yaw_rad': .1},
        'manipulation': {'translation_m': [.005, 0, 0]},
    })
    active = {'planning', 'navigating', 'aligning', 'parking', 'manipulation_planning'}
    deadline = time.monotonic() + 45
    try:
        while task['status'] in active:
            if time.monotonic() > deadline:
                request('/v1/navigation-cancel', {'task_id': task['task_id']})
                raise RuntimeError('Client timeout; task canceled')
            time.sleep(.1)
            task = request('/v1/navigation-task/' + task['task_id'])
    except KeyboardInterrupt:
        request('/v1/navigation-cancel', {'task_id': task['task_id']})
        raise
    if task['status'] != 'succeeded':
        raise RuntimeError(json.dumps(task, ensure_ascii=False))
    nav, arm = task['navigation'], task['result']
    print(json.dumps({
        'status': task['status'], 'task_id': task['task_id'],
        'drive_type': nav['drive_type'], 'parking_confirmed': nav['parking_confirmed'],
        'stable_stop_s': nav['stable_stop_s'], 'base_pose': nav['base_pose'],
        'arm_samples': arm['validated_samples'],
        'navigation_map_checked': arm['navigation_map_checked'],
        'max_tcp_position_error_m': arm['max_tcp_position_error_m'],
    }, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
