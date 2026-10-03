"""Manage an explicit skill registry. Never download, execute or install skills."""
import argparse
import hashlib
import json
import re
from pathlib import Path

def files_digest(folder):
    result = {}
    for path in sorted(folder.rglob('*')):
        if path.is_symlink():
            raise ValueError('Symlinks are not accepted in bundled skills')
        if path.is_file() and '__pycache__' not in path.parts and path.suffix != '.pyc':
            result[path.relative_to(folder).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    return dict(sorted(result.items()))

def read_registry(repo):
    data = json.loads((repo / 'skills.lock.json').read_text())
    if data.get('schema_version') != 1 or not isinstance(data.get('skills'), dict):
        raise ValueError('Unsupported or invalid registry')
    return data

def folder_for(repo, name):
    if len(name) > 64 or not re.fullmatch('[a-z0-9]+(?:-[a-z0-9]+)*', name):
        raise ValueError('Invalid skill name')
    folder = repo / 'skills' / name
    if folder.is_symlink() or not folder.resolve().is_relative_to(repo.resolve()):
        raise ValueError('Skill path escapes repository')
    content = (folder / 'SKILL.md').read_text()
    header = re.match(r'\A---\n(.*?)\n---', content, re.S)
    if not header:
        raise ValueError('Missing frontmatter')
    content = header[1]
    if not re.search(r'^name:\s*' + re.escape(name) + r'\s*$', content, re.M):
        raise ValueError('Skill frontmatter name does not match directory')
    if not re.search(r'^description:\s*\S', content, re.M):
        raise ValueError('Missing skill description')
    return folder

def verify(repo):
    data = read_registry(repo)
    errors = []
    actual = {p.name for p in (repo / 'skills').iterdir() if (p / 'SKILL.md').is_file()}
    if actual != set(data['skills']):
        errors.append('Registry and skill directories differ')
    for name, entry in data['skills'].items():
        try:
            folder = folder_for(repo, name)
            if entry.get('path') != 'skills/' + name:
                raise ValueError('Invalid registered path')
            if not entry.get('when') or not entry.get('role'):
                raise ValueError('Missing routing role/when')
            if entry.get('kind') not in ('first-party', 'vendored'):
                raise ValueError('Invalid skill kind')
            if entry['kind'] == 'vendored':
                if not re.fullmatch('[0-9a-f]{40}', entry.get('source_ref', '')):
                    raise ValueError('Vendored source must use a full commit SHA')
                if not (folder / 'LICENSE').is_file() or not entry.get('source_url') or not entry.get('license'):
                    raise ValueError('Missing source or license')
            if files_digest(folder) != entry.get('sha256'):
                raise ValueError('File integrity mismatch; review changes before updating registry')
        except (OSError, ValueError) as exc:
            errors.append(name + ': ' + str(exc))
    return errors

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, required=True)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('verify')
    sub.add_parser('list')
    refresh = sub.add_parser('refresh')
    refresh.add_argument('--name', required=True)
    register = sub.add_parser('register')
    register.add_argument('--name', required=True)
    register.add_argument('--role', required=True)
    register.add_argument('--when', required=True)
    register.add_argument('--source-url', required=True)
    register.add_argument('--source-ref', required=True)
    register.add_argument('--license', required=True)
    args = parser.parse_args()
    try:
        data = read_registry(args.repo)
        if args.command == 'verify':
            errors = verify(args.repo)
            print(json.dumps({'ok': not errors, 'errors': errors}, ensure_ascii=False, indent=2))
            raise SystemExit(bool(errors))
        if args.command == 'list':
            print('\n'.join(data['skills']))
            return
        name = args.name
        folder = folder_for(args.repo, name)
        if args.command == 'refresh':
            if data['skills'].get(name, {}).get('kind') != 'first-party':
                raise ValueError('Only first-party files may be refreshed; upstream updates require review')
            data['skills'][name]['sha256'] = files_digest(folder)
            if (folder / 'VERSION').is_file():
                data['skills'][name]['version'] = (folder / 'VERSION').read_text().strip()
        else:
            if name in data['skills']:
                raise ValueError('Already registered; do not overwrite an existing skill')
            if not re.fullmatch('[0-9a-f]{40}', args.source_ref):
                raise ValueError('Source ref must be a full commit SHA')
            if not (folder / 'LICENSE').is_file():
                raise ValueError('Retain the original LICENSE before registration')
            data['skills'][name] = {'kind': 'vendored', 'path': 'skills/' + name,
                'role': args.role, 'when': args.when, 'source_url': args.source_url,
                'source_ref': args.source_ref, 'license': args.license, 'sha256': files_digest(folder)}
        (args.repo / 'skills.lock.json').write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
        print('Registry updated; not installed or published.')
    except (OSError, ValueError, KeyError) as exc:
        parser.exit(1, str(exc) + '\n')

if __name__ == '__main__':
    main()
