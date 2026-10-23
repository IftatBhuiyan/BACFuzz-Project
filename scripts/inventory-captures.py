#!/usr/bin/env python3
"""Inventory a private CVE_2025_0802 collection without printing request contents.

Reads YAML nodes without constructing Python objects. This is a completeness
check, not login verification, a redactor, or proof of an authorization flaw.
"""
import argparse
from collections import Counter
import json
from pathlib import Path

import yaml
from yaml.nodes import MappingNode, ScalarNode

ROLES = ('Admin', 'LeaveManager', 'Salary', 'BorrowManager', 'Anonymous')
METHODS = frozenset(('GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH'))
MAX_BYTES = 2 * 1024 * 1024


def request_method(path):
    if path.is_symlink() or not path.is_file():
        raise ValueError('not a regular capture')
    with path.open('rb') as stream:
        raw = stream.read(MAX_BYTES + 1)
    if len(raw) > MAX_BYTES:
        raise ValueError('capture exceeds limit')
    # compose returns syntax nodes; it never invokes Python object constructors,
    # including tags used for nested ParamValue objects in upstream YAML.
    node = yaml.compose(raw, Loader=yaml.SafeLoader)
    if not isinstance(node, MappingNode) or node.tag != 'tag:yaml.org,2002:map':
        raise ValueError('capture root must be a mapping')
    fields = {}
    for key, value in node.value:
        if not isinstance(key, ScalarNode):
            raise ValueError('non-scalar key')
        if key.value in fields:
            raise ValueError('duplicate key')
        fields[key.value] = value
    method = fields.get('method')
    if not isinstance(method, ScalarNode) or method.tag != 'tag:yaml.org,2002:str' or method.value not in METHODS:
        raise ValueError('missing or unsupported method')
    for name in ('url', 'full_url'):
        value = fields.get(name)
        if not isinstance(value, ScalarNode) or value.tag != 'tag:yaml.org,2002:str' or not value.value:
            raise ValueError('missing URL')
    return method.value


def inventory(root):
    result = {'target': 'CVE_2025_0802', 'roles': {}, 'dictionary_present': False,
              'unexpected_entries': 0, 'complete': False}
    if root.is_symlink() or not root.is_dir():
        raise ValueError('Collection must be a real directory')
    result['unexpected_entries'] = sum(p.name not in (*ROLES, 'paramval.yaml') for p in root.iterdir())
    dictionary = root / 'paramval.yaml'
    result['dictionary_present'] = dictionary.is_file() and not dictionary.is_symlink() and dictionary.stat().st_size > 0
    for role in ROLES:
        directory = root / role
        row = {'present': directory.is_dir() and not directory.is_symlink(),
               'valid_captures': 0, 'rejected_entries': 0, 'methods': {}}
        if row['present']:
            methods = Counter()
            for path in directory.iterdir():
                try:
                    if path.suffix != '.yaml' or not path.stem.isascii() or not path.stem.isdigit():
                        raise ValueError('unexpected entry')
                    methods[request_method(path)] += 1
                    row['valid_captures'] += 1
                except (OSError, ValueError, yaml.YAMLError, RecursionError):
                    # Never echo parser errors, filenames or YAML; they may contain tokens.
                    row['rejected_entries'] += 1
            row['methods'] = dict(sorted(methods.items()))
        result['roles'][role] = row
    result['complete'] = bool(result['dictionary_present'] and not result['unexpected_entries'] and all(
        r['present'] and r['valid_captures'] and not r['rejected_entries'] for r in result['roles'].values()))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('collection', type=Path, help='Private attack_surface/CVE_2025_0802 directory')
    args = parser.parse_args()
    try:
        result = inventory(args.collection)
    except (OSError, ValueError):
        print(json.dumps({'complete': False, 'error': 'Collection directory unavailable or unsupported'}))
        return 1
    print(json.dumps(result, indent=2))
    return 0 if result['complete'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
