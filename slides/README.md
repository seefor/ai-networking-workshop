# Workshop Slides

Slidev presentation for the AI Networking Workshop.

## Quick Start

### Install Slidev

```bash
npm install -g @slidev/cli
```

### Run Presentation

```bash
cd slides
slidev slides.md
```

This will open the presentation at `http://localhost:3030`

## Features

- **Interactive slides** with live coding examples
- **Code highlighting** with syntax support
- **Click-through animations** for progressive disclosure
- **Speaker notes** for instructor guidance
- **PDF export** for distribution

## Export Options

### Export to PDF

```bash
slidev export slides.md --format pdf
```

### Export to PNG (individual slides)

```bash
slidev export slides.md --format png
```

### Export to HTML (static site)

```bash
slidev build slides.md
```

## Slide Structure

The slides are organized into modules matching the workshop structure:

- **Module 0:** Welcome & Setup (10 min)
- **Module 1:** How LLMs Work (25 min)
- **Lab 1:** Ollama + Network Prompts (20 min)
- **Module 2:** Prompt Engineering (20 min)
- **Lab 2:** P.E.N.E. Framework (20 min)
- **Module 3:** LLM APIs & Tool Calling (20 min)
- **Lab 3:** Network Chatbot (20 min)
- **Lab 4:** Agentic Network Bot (20 min)
- **Break:** 10 min
- **Module 4:** MCP Protocol (20 min)
- **Lab 5:** MCP Server (25 min)
- **Lab 6:** Integration (15 min)
- **Wrap-Up:** Q&A (10 min)

## Key Updates (April 2026)

**✅ Updated for mock device approach:**
- Removed Docker/Containerlab references
- Added mock network device explanations
- Included production migration examples
- Simplified prerequisites

**Mock vs Production sections:**
- Shows side-by-side code comparison
- Explains agent code portability
- Demonstrates minimal changes needed

## Customization

### Theme

Current theme: `default`

To change:
```yaml
---
theme: seriph  # or any other Slidev theme
---
```

### Fonts

Configured in slides frontmatter:
```yaml
fonts:
  sans: 'Roboto'
  serif: 'Roboto Slab'
  mono: 'Fira Code'
```

### Colors

Using Tailwind CSS classes throughout. Customize in `slides.md`.

## Tips for Presenting

### Navigation

- **Arrow keys:** Next/previous slide
- **Space:** Next slide
- **Shift+Space:** Previous slide
- **G:** Go to slide number
- **O:** Overview mode
- **F:** Fullscreen
- **ESC:** Exit fullscreen/overview

### Presenter Mode

Press **P** to open presenter view in a new window:
- Shows current slide + next slide
- Speaker notes visible
- Timer for pacing

### Drawing Mode

Press **D** to enable drawing on slides:
- Annotate live during presentation
- Clear with **C**
- Great for highlighting code

## Code Examples

All code examples are syntax-highlighted and formatted for readability.

**Tip:** Use `v-click` animations to reveal code incrementally.

## Links and Resources

Slides include links to:
- GitHub repository
- Documentation
- MCP specification
- Anthropic docs
- External resources

## Troubleshooting

**Slides not loading?**
```bash
npm install
slidev slides.md
```

**Port already in use?**
```bash
slidev slides.md --port 3031
```

**PDF export not working?**
```bash
npm install -g playwright-chromium
slidev export slides.md --format pdf
```

## Distribution

**For attendees:**
- Share PDF export (no dependencies)
- Share GitHub repository link
- Provide access to slide deck source

**For instructors:**
- Keep slides.md source
- Use presenter mode
- Enable drawing for annotations

---

**Workshop:** AI Networking Workshop: From LLMs to Production Agents  
**Date:** March 31, 2026  
**Duration:** 3.25 hours  
**Format:** Slidev presentation
