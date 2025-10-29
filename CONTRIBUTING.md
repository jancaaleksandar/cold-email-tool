# Contributing to Clay Clone

Thank you for considering contributing to Clay Clone! This document provides guidelines and instructions for contributing.

## 🏗️ Development Setup

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- Git

### Local Setup

1. **Fork and clone the repository**
```bash
git clone https://github.com/yourusername/clay-clone.git
cd clay-clone
```

2. **Set up backend**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your API keys
```

3. **Set up frontend**
```bash
cd frontend
npm install
cp .env.local.example .env.local
```

4. **Start databases**
```bash
docker run -d -p 5432:5432 -e POSTGRES_USER=clay_user -e POSTGRES_PASSWORD=clay_password -e POSTGRES_DB=clay_clone postgres:15-alpine
docker run -d -p 6379:6379 redis:7-alpine
```

## 📝 Code Style

### Python (Backend)
- Follow PEP 8
- Use type hints
- Maximum line length: 100 characters
- Use meaningful variable names
- Add docstrings to functions

Example:
```python
async def enrich_lead(lead_id: int, enrichment_type: str) -> Dict[str, Any]:
    """
    Enrich a lead with specified enrichment type.
    
    Args:
        lead_id: ID of the lead to enrich
        enrichment_type: Type of enrichment (apollo, email, ai, scraper)
        
    Returns:
        Dictionary containing enrichment results
    """
    # Implementation
```

### TypeScript (Frontend)
- Use TypeScript for type safety
- Follow Airbnb style guide
- Use functional components
- Prefer const over let
- Use meaningful component names

Example:
```typescript
interface LeadProps {
  lead: Lead
  onUpdate: (lead: Lead) => void
}

export default function LeadCard({ lead, onUpdate }: LeadProps) {
  // Implementation
}
```

## 🔄 Git Workflow

### Branch Naming
- `feature/` - New features
- `fix/` - Bug fixes
- `refactor/` - Code refactoring
- `docs/` - Documentation updates
- `test/` - Test additions or updates

Examples:
- `feature/add-linkedin-scraper`
- `fix/email-validation-bug`
- `refactor/api-client-structure`

### Commit Messages
Follow conventional commits:

```
type(scope): subject

body (optional)

footer (optional)
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Examples:
```
feat(enrichment): add LinkedIn profile scraping

- Implement LinkedIn scraper service
- Add rate limiting
- Update API endpoints

Closes #123
```

```
fix(upload): handle CSV parsing errors

Properly catch and display CSV parsing errors to users
instead of showing generic error message.
```

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest

# With coverage
pytest --cov=. --cov-report=html
```

### Frontend Tests
```bash
cd frontend
npm test

# With coverage
npm test -- --coverage
```

### Manual Testing
1. Start all services
2. Upload sample CSV from `data/sample_leads.csv`
3. Test enrichment with all types
4. Verify error handling
5. Check responsive design on mobile

## 📦 Adding New Features

### Adding a New Enrichment Service

1. **Create service file**
```python
# backend/services/new_service.py
class NewEnrichmentService:
    def __init__(self):
        self.api_key = os.getenv("NEW_SERVICE_API_KEY")
    
    async def enrich(self, lead_data: Dict) -> Dict:
        # Implementation
        pass
```

2. **Add to Celery tasks**
```python
# backend/workers/tasks.py
def enrich_new_service(lead: Lead, db: Session) -> dict:
    service = NewEnrichmentService()
    result = asyncio.run(service.enrich(lead_data))
    return result

# Add to enrich_lead_task switch statement
elif enrichment_type == "new_service":
    result = enrich_new_service(lead, db)
```

3. **Update dependencies**
```
# backend/requirements.txt
new-service-sdk==1.0.0
```

4. **Add environment variables**
```bash
# .env.example
NEW_SERVICE_API_KEY=your_key_here
```

5. **Update documentation**
- Add to README.md
- Add to PROJECT_SUMMARY.md
- Document API key setup

### Adding a New Frontend Component

1. **Create component**
```tsx
// frontend/components/NewComponent.tsx
'use client'

import { useState } from 'react'

interface NewComponentProps {
  // Props
}

export default function NewComponent({ }: NewComponentProps) {
  // Implementation
  return <div>...</div>
}
```

2. **Add types**
```typescript
// frontend/lib/types.ts
export interface NewType {
  // Fields
}
```

3. **Update API client if needed**
```typescript
// frontend/lib/api.ts
export const newApiCall = async (): Promise<NewType> => {
  const response = await api.get('/api/new-endpoint')
  return response.data
}
```

## 🐛 Bug Reports

When reporting bugs, include:

1. **Description**: Clear description of the bug
2. **Steps to Reproduce**: Detailed steps
3. **Expected Behavior**: What should happen
4. **Actual Behavior**: What actually happens
5. **Environment**: OS, browser, versions
6. **Screenshots**: If applicable
7. **Logs**: Relevant error logs

Use the bug report template:

```markdown
## Bug Description
Brief description here

## Steps to Reproduce
1. Go to '...'
2. Click on '...'
3. Scroll down to '...'
4. See error

## Expected Behavior
What you expected to happen

## Actual Behavior
What actually happened

## Environment
- OS: macOS 13.0
- Browser: Chrome 120
- Node: 18.17.0
- Python: 3.11.5

## Screenshots
[If applicable]

## Additional Context
Any other relevant information
```

## 💡 Feature Requests

When requesting features, include:

1. **Problem**: What problem does this solve?
2. **Solution**: Proposed solution
3. **Alternatives**: Alternative solutions considered
4. **Additional Context**: Mockups, examples, etc.

## 🔍 Code Review Process

### For Contributors
1. Ensure all tests pass
2. Update documentation
3. Follow code style guidelines
4. Keep PRs focused and small
5. Respond to review comments

### For Reviewers
- Be constructive and kind
- Explain reasoning for changes
- Approve when satisfied
- Test changes locally if needed

## 📋 Pull Request Checklist

Before submitting a PR, ensure:

- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] No linting errors
- [ ] Commit messages follow convention
- [ ] Branch is up to date with main
- [ ] PR description is clear

## 🎯 Areas for Contribution

### High Priority
- [ ] User authentication and authorization
- [ ] Team management features
- [ ] Advanced export options
- [ ] Campaign management
- [ ] Analytics dashboard

### Medium Priority
- [ ] Email sequence automation
- [ ] Webhook integrations
- [ ] CRM integrations (Salesforce, HubSpot)
- [ ] Mobile app
- [ ] Advanced filtering and search

### Good First Issues
- [ ] Improve error messages
- [ ] Add more sample CSVs
- [ ] Enhance UI components
- [ ] Add tooltips and help text
- [ ] Improve documentation

## 📞 Getting Help

- **Documentation**: Check README.md and docs/
- **Issues**: Search existing issues first
- **Discussions**: Use GitHub Discussions for questions
- **Discord**: Join our Discord server (if available)

## 📄 License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT License).

## 🙏 Recognition

Contributors will be:
- Added to CONTRIBUTORS.md
- Mentioned in release notes
- Credited in documentation

Thank you for contributing to Clay Clone! 🚀

