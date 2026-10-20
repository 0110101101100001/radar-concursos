#!/usr/bin/env node

const { execSync, spawn } = require('child_process');
const path = require('path');

const BOLD = '\x1b[1m';
const BLUE = '\x1b[34m';
const RESET = '\x1b[0m';
const GRAY = '\x1b[90m';

let python;
try {
  execSync('python3 --version', { stdio: 'pipe' });
  python = 'python3';
} catch (_) {
  python = 'python';
}

const script = path.join(__dirname, '..', 'main.py');
const args = process.argv.slice(2);

if (args.length === 0) {
  process.stdout.write(`${BLUE}${BOLD}radar-concursos${RESET}\n`);
  process.stdout.write(`${GRAY}  python main.py${RESET}\n`);
  process.stdout.write(`${GRAY}  npx .${RESET}\n\n`);
  process.exit(0);
}

const child = spawn(python, [script, ...args], { stdio: 'inherit' });
child.on('exit', (code) => {
  process.exit(code || 0);
});
