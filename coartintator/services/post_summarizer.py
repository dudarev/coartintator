from abc import ABC, abstractmethod

import dotenv

from coartintator.entities import Post, PostSummary


import anthropic

dotenv.load_dotenv()


# defaults to os.environ.get("ANTHROPIC_API_KEY")
client = anthropic.Anthropic()

MODEL = "claude-3-haiku-20240307"
MAX_TOKENS = 1000
TEMPERATURE = 0.0
SYSTEM = "Summarize the content in bullet points in Markdown format. Return only the summary without introduction or conclusion."


class AbstractPostSummarizer(ABC):
    @abstractmethod
    def summarize(self, post: Post) -> PostSummary:
        pass


class DummyPostSummarizer(AbstractPostSummarizer):
    def summarize(self, post: Post) -> PostSummary:
        return PostSummary(post=post, summary="Dummy summary")


class ClaudeHaikuSummarizer(AbstractPostSummarizer):
    def summarize(self, post: Post) -> PostSummary:
        message = client.messages.create(
            model=MODEL,
            max_tokens=MAX_TOKENS,
            temperature=TEMPERATURE,
            system=SYSTEM,
            messages=[{"role": "user", "content": post.content}],
        )
        summary = message.content[0].text
        print(summary)
        return PostSummary(post=post, summary=summary)


if __name__ == "__main__":
    print("Running post summarizer")
    summarizer = ClaudeHaikuSummarizer()
    post = Post(
        name="Test", title="Test", url="https://example.com", content="This is a test"
    )
    summary = summarizer.summarize(post)
    print(summary.summary)
    print("Done")
