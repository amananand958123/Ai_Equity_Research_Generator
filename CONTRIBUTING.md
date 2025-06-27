# Contributing to Equity Research Report Generator

Thank you for your interest in contributing to the Equity Research Report Generator! This document provides guidelines for contributing to the project.

## Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct. We expect all contributors to be respectful and constructive in their interactions.

## How to Contribute

### Reporting Issues

1. **Search existing issues** first to avoid duplicates
2. **Use the issue template** when creating new issues
3. **Provide detailed information** including:
   - Steps to reproduce the issue
   - Expected vs actual behavior
   - Environment details (OS, Python version, Node.js version)
   - Error messages or screenshots

### Suggesting Enhancements

1. **Check the roadmap** to see if your idea is already planned
2. **Open an issue** with the "enhancement" label
3. **Describe your suggestion** clearly with:
   - Use case and benefits
   - Proposed implementation approach
   - Any alternatives considered

### Pull Requests

1. **Fork the repository** and create a feature branch
2. **Follow the coding standards** outlined below
3. **Write tests** for new functionality
4. **Update documentation** as needed
5. **Submit a pull request** with a clear description

## Development Setup

### Prerequisites
- Python 3.8+
- Node.js 16+
- Git

### Local Development

```bash
# Fork and clone the repository
git clone https://github.com/yourusername/equity-research-generator.git
cd equity-research-generator

# Set up backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Set up frontend  
cd frontend
npm install
cd ..

# Copy environment template
cp .env.example .env
# Add your API keys to .env

# Start development servers
./start-servers.sh
```

## Coding Standards

### Python Code
- Follow **PEP 8** style guidelines
- Use **type hints** where appropriate
- Write **docstrings** for functions and classes
- Keep functions focused and modular
- Use meaningful variable and function names

### TypeScript/React Code
- Follow **ESLint** and **Prettier** configurations
- Use **TypeScript** for type safety
- Write **JSDoc** comments for complex functions
- Use **functional components** with hooks
- Follow React best practices

### General Guidelines
- **Keep commits atomic** - one logical change per commit
- **Write clear commit messages** using conventional commits format
- **Test your changes** thoroughly before submitting
- **Update documentation** for any user-facing changes

## Testing

### Backend Tests
```bash
# Run Python tests
python -m pytest tests/

# Test API endpoints
./test-api.sh

# Verify report content
python verify_report_content.py
```

### Frontend Tests
```bash
cd frontend
npm test
npm run lint
npm run type-check
```

## Documentation

- Keep the README.md up to date
- Document new features in the appropriate sections
- Include code examples for new APIs
- Update the changelog for significant changes

## Project Structure

### Backend Components
- `bridge_server.py` - Flask API server
- `comprehensive_report_generator.py` - Core report engine
- `data_aggregator.py` - Data collection and processing
- `advanced_visualizer.py` - Chart generation

### Frontend Components
- `src/app/` - Next.js app router pages
- `src/components/` - Reusable React components
- `src/api/` - API route handlers

## Areas for Contribution

### High Priority
- [ ] ESG (Environmental, Social, Governance) analysis
- [ ] Sector comparison and peer analysis
- [ ] International market support expansion
- [ ] Performance optimizations
- [ ] Test coverage improvements

### Medium Priority
- [ ] Additional chart types and visualizations
- [ ] Real-time notifications and alerts
- [ ] Portfolio analysis features
- [ ] Mobile responsiveness improvements
- [ ] Documentation enhancements

### Low Priority
- [ ] Theme customization
- [ ] Additional export formats
- [ ] Localization/internationalization
- [ ] Browser extension
- [ ] Desktop application

## Getting Help

- **Documentation**: Check the [docs/](docs/) directory
- **Issues**: Search existing issues or create a new one
- **Discussions**: Use GitHub Discussions for questions
- **Email**: Contact the maintainers directly for sensitive matters

## Recognition

Contributors will be recognized in:
- The project README
- Release notes for significant contributions
- A separate CONTRIBUTORS.md file

## License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to the Equity Research Report Generator! 🚀
