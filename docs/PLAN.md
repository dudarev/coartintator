# Plan

## Commands

- Implement a question command `QQ: {question}` that can be used in summaries to ask questions about posts
- `IMP` - improve command
- Allow to modify SUM command prompt in a Markdown file
- Allow to create custom commands in a Markdown file in `commands/` directory:
  - Commands configuration:
    - acts till end of file
    - acts on paragraph
    - acts till next command
    - response overrides the paragraph or appends to it
    - LLM models to use

## Feeds

- Add new feed types:
  - Manual feed without crawling, just a collection of links
  - RSS/Atom
  - Twitter account/list
  - Reddit post

## AI/LLM

- More models to use
  - More from Anthropic, especiall Opus
  - OpenAI
  - Mistral
  - Local models
    - Llama
    - Mistral

## Other Enhancements

- Implement `last_crawled_at` property for feeds
  - Implement filter logic when determining which feeds to update
