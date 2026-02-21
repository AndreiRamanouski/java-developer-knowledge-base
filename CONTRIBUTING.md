# Contributing to Java Developer Knowledge Base

Thank you for considering a contribution! This project grows through community input, and every improvement — no matter how small — makes a difference.

---

## 📋 Before You Start

1. Check existing issues and PRs to avoid duplicate work
2. For large additions (new sections or topics), open an issue first to discuss
3. For small fixes (typos, code corrections, clarifications), just open a PR directly

---

## ✅ Content Standards

To keep the knowledge base consistent and high quality, please follow these guidelines:

### Format
- All files are written in **Markdown**
- Follow the structure of existing files in the same section
- Use headers consistently: `##` for main sections, `###` for subsections
- Code examples must be in fenced code blocks with the language specified

  ````markdown
  ```java
  // your code here
  ```
  ````

### Code Examples
- Use **Java 17+** unless the topic specifically requires an older version
- Spring Boot examples should use **Spring Boot 3.x**
- All code examples must be correct and runnable
- Include comments that explain non-obvious parts
- Prefer practical, real-world examples over toy examples

### Writing Style
- Write from a **practitioner's perspective** — explain the "why", not just the "what"
- Use analogies where helpful (e.g. the Java class/object analogy for Docker images/containers)
- Avoid marketing language — be direct and honest about tradeoffs
- Include warnings and gotchas where relevant (mark with ⚠️)

---

## 🗂️ File Structure

Each topic file should follow this general structure:

```
## Overview
Brief intro to the topic

## Core Concepts
Key concepts explained with examples

## Code Examples
Practical, working examples

## Common Pitfalls
Things to watch out for (use ⚠️)

## Best Practices
Recommended approaches

```

You don't need all sections for every PR — even a single well-written section is a valid contribution.

---

## 🚀 How to Submit a PR

1. **Fork** the repository
2. **Create a branch** with a descriptive name:
   ```
   git checkout -b add-redis-nosql-section
   git checkout -b fix-kafka-consumer-example
   ```
3. **Make your changes**
4. **Commit** with a clear message:
   ```
   git commit -m "Add Redis section to NoSQL guide"
   git commit -m "Fix incorrect Kafka consumer group example"
   ```
5. **Push** and open a Pull Request against `main`
6. Fill out the PR template

---

## 🚫 What We Don't Accept

- Content copied directly from official documentation without transformation
- AI-generated content that hasn't been reviewed and validated by a human
- Topics unrelated to Java backend development
- Self-promotional content or links

---

## 💬 Questions?

Open an issue with the `question` label and we'll get back to you.