#!/bin/bash

echo "🐍 Python Development Environment Setup with uv"
echo "=============================================="

# 1. Check prerequisites
if ! command -v code &> /dev/null; then
    echo "❌ VS Code CLI not found"
    exit 1
fi

if ! command -v uv &> /dev/null; then
    echo "❌ uv not found. Installing..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi

# 2. Install VS Code extensions
echo "📦 Installing VS Code extensions..."
code --install-extension ms-python.python
code --install-extension ms-python.vscode-pylance
code --install-extension ms-python.black-formatter
code --install-extension ms-toolsai.jupyter

# 3. Initialize uv project (creates pyproject.toml)
echo ""
echo "🚀 Initializing uv project..."
if [ ! -f "pyproject.toml" ]; then
    uv init
fi

# 4. Add development dependencies
echo "📚 Adding Python packages with uv..."
uv add --dev pylint black pytest pytest-cov isort

# 5. Create virtual environment and sync
echo "🔧 Creating virtual environment..."
uv venv
source .venv/bin/activate

# 6. Create VS Code settings (using uv's Python path)
mkdir -p .vscode

cat > .vscode/settings.json << 'EOF'
{
    // Use uv's virtual environment
    "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
    "python.terminal.activateEnvironment": true,

    // Pylint setup
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.linting.pylintArgs": [
        "--max-line-length=100",
        "--disable=C0114,C0115,C0116",
        "--good-names=i,j,k,ex,Run,_"
    ],

    // Black formatting
    "[python]": {
        "editor.defaultFormatter": "ms-python.black-formatter",
        "editor.formatOnSave": true,
        "editor.codeActionsOnSave": {
            "source.organizeImports": "explicit"
        }
    },

    "python.formatting.provider": "black",
    "python.formatting.blackArgs": [
        "--line-length", "100",
        "--target-version", "py39"
    ],

    // Testing with pytest
    "python.testing.pytestEnabled": true,
    "python.testing.autoTestDiscoverOnSaveEnabled": true,
    "python.testing.pytestArgs": ["-v", "--maxfail=5"],

    // Editor settings
    "editor.rulers": [100],
    "files.trimTrailingWhitespace": true,
    "files.insertFinalNewline": true
}
EOF

# 7. Configure pyproject.toml for your tools
cat >> pyproject.toml << 'EOF'

[tool.black]
line-length = 100
target-version = ['py39']
skip-string-normalization = true

[tool.pylint]
max-line-length = 100
good-names = ["i", "j", "k", "ex", "Run", "_"]
disable = ["C0114", "C0115", "C0116"]

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --tb=short"
EOF

echo ""
echo "✅ Setup complete with uv!"
echo "================================================"
echo "📋 Key uv commands:"
echo "   uv add <package>     # Add a dependency"
echo "   uv sync              # Sync environment"
echo "   uv run pytest        # Run tests"
echo "   uv tree              # View dependencies"
echo ""
echo "🎯 Your pyproject.toml is now the single source of truth!"
