#!/usr/bin/env node
const { spawnSync } = require('child_process');
const path = require('path');

// Encontra o caminho absoluto para o teu main.py
const scriptPath = path.join(__dirname, '..', 'main.py');

// Executa o Python e cede o controlo do terminal para a TUI
const result = spawnSync('python', [scriptPath], { stdio: 'inherit' });

// Garante que o processo termina corretamente se saíres da TUI
process.exit(result.status);