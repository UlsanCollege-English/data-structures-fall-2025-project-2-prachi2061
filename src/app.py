"""
Interactive CLI entrypoint.
Commands:
  load <path>
  save <path>
  insert <word> <freq>
  remove <word>
  contains <word>
  complete <prefix> <k>
  stats
  quit
"""

import sys
from trie import Trie           # ✅ Changed from 'src.trie' to 'trie'
from io_utils import load_csv, save_csv  # ✅ Changed from 'src.io_utils' to 'io_utils'

PROMPT = ""  # keep outputs machine-friendly (no prompt)

def main():
    trie = Trie()

    for line in sys.stdin:
        try:
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            cmd = parts[0].lower()

            if cmd == 'quit':
                break

            elif cmd == 'load' and len(parts) == 2:
                path = parts[1]
                pairs = load_csv(path)
                trie = Trie()  # Reset trie
                for w, s in pairs:
                    trie.insert(w, s)

            elif cmd == 'save' and len(parts) == 2:
                path = parts[1]
                save_csv(path, trie.items())

            elif cmd == 'insert' and len(parts) == 3:
                w = parts[1].lower()
                freq = float(parts[2])
                trie.insert(w, freq)

            elif cmd == 'remove' and len(parts) == 2:
                w = parts[1].lower()
                print('OK' if trie.remove(w) else 'MISS')

            elif cmd == 'contains' and len(parts) == 2:
                w = parts[1].lower()
                print('YES' if trie.contains(w) else 'NO')

            elif cmd == 'complete' and len(parts) == 3:
                prefix = parts[1].lower()
                k = int(parts[2])
                results = trie.complete(prefix, k)
                print(','.join(results))

            elif cmd == 'stats':
                words, height, nodes = trie.stats()
                print(f"words={words} height={height} nodes={nodes}")

            # Unknown or malformed commands are ignored

        except Exception as e:
            print(f"ERROR: {e}", file=sys.stderr)

if __name__ == '__main__':
    main()