#!/bin/bash
# setup.sh - Sets up Python development environment with uv

echo "🐍 Python Development Environment Setup with uv"
echo "=============================================="

# 1. Install uv if not present
if ! command -v uv &> /dev/null; then
    echo "📦 Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    source ~/.local/bin/env
fi

# 2. Install VS Code extensions (if VS Code is installed)
if command -v code &> /dev/null; then
    echo "📦 Installing VS Code extensions..."
    code --install-extension ms-python.python
    code --install-extension ms-python.vscode-pylance
    code --install-extension ms-python.black-formatter
    code --install-extension ms-toolsai.jupyter
else
    echo "⚠️ VS Code not found - skipping extension installation"
fi

# 3. Create pyproject.toml if it doesn't exist
if [ ! -f "pyproject.toml" ]; then
    echo "📝 Creating pyproject.toml..."
    uv init
fi

# 4. Add dependencies
echo "📚 Adding Python packages..."
uv add pandas langchain langchain-ollama sentence-transformers chromadb
uv add --dev pylint black pytest pytest-cov isort

# 5. Sync environment
echo "🔧 Creating virtual environment and syncing dependencies..."
uv sync

# 6. Create VS Code settings
mkdir -p .vscode
cat > .vscode/settings.json << 'EOF'
{
    "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
    "python.terminal.activateEnvironment": true,
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.linting.pylintArgs": [
        "--max-line-length=100",
        "--disable=C0114,C0115,C0116",
        "--good-names=i,j,k,ex,Run,_"
    ],
    "[python]": {
        "editor.defaultFormatter": "ms-python.black-formatter",
        "editor.formatOnSave": true,
        "editor.codeActionsOnSave": {
            "source.organizeImports": "explicit"
        }
    },
    "editor.rulers": [100],
    "files.trimTrailingWhitespace": true,
    "files.insertFinalNewline": true
}
EOF

echo ""
echo "✅ Python development environment ready!"
echo ""
echo "📋 Next steps:"
echo "   1. Install Ollama from https://ollama.com"
echo "   2. Run: ollama pull llama3.2"
echo "   3. Run: uv run python main.py"
