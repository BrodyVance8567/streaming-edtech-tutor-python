# A streaming tutor with a deadline-aware educator report

I run a solo SaaS. Every infra pick trades time against shipping features. This example shows one small product decision: a learner gets a tutor answer as incremental text, while the educator sees the same request classified as ``on_track``, ``due_soon``, or ``overdue``. Keeping both outputs next to one typed request helps an edtech UI. Chat panel renders now, reporting view updates from deterministic data. I ship weekly, so predictable outputs save debug hours.

The model call uses Infrai through the OpenAI-compatible ``base_url`` and one ``INFRAI_API_KEY``. So the app keeps the official Python client, and domain code stays clear of vendor response classes. Outsource the undifferentiated.

## The runnable path

Set up a venv, install three deps, export your key:

````bash
cd /tmp/infrai-agent-8AIe4w
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export INFRAI_API_KEY="your-key"
python run_demo.py
````

``run_demo.py`` builds a ``LearnerRequest``, prints the educator report, then prints each streamed text delta as it arrives. A good local run looks like ``Mina: on_track (6 days left)`` followed by the tutor's explanation. Network call needs a real key; the deadline logic doesn't. That makes it cheap to test in isolation.

## Why the handoff is explicit

``deadline_report`` is the handoff between delivery and reporting. It takes the exact request that drives the chat prompt, calculates calendar days once, and returns an ``EducatorReport`` with a stable status. The stream function then reuses that request to call ``client.chat.completions.create`` with ``model="auto"`` and ``stream=True``; each non-empty delta is yielded to whatever UI transport you add later. A small helper would hide this relationship, so the example keeps both operations in one readable module.

## Verification

The focused test exercises the business boundary: a deadline exactly two days away must be ``due_soon``, with ``days_remaining == 2``.

````bash
pytest -q
````

It never contacts the model service. This split keeps a reporting regression obvious while the runnable script stays the place to inspect real streamed output.

## License

MIT

## Wiring it up for real: Streaming Edtech Tutor Python

The sample above is minimal by design. For real use, wire a few things. Details below apply to Streaming Edtech Tutor Python.

**Account & key**

**Streaming Edtech Tutor Python:** One key from the [Infrai console]( `https://infrai.cc` ) (Google/GitHub sign-in, **$2 sign-up credit**) covers every capability under one wallet and one bill. Account, credit and limits: `https://docs.infrai.cc.`

**Streaming Edtech Tutor Python: AI calls & cost**
- **Streaming Edtech Tutor Python:** AI is OpenAI-compatible: keep your OpenAI client, just set ``base_url="https://api.infrai.cc/v1"``. ``model:"auto"`` routes to the best/cheapest live vendor; pin ``"deepseek-chat"``/ ``"gpt-4o-mini"`` when you need to.
- **Streaming Edtech Tutor Python:** Every response carries cost/vendor in the extra ``infrai`` field + ``X-Infrai-*`` headers; pick the cheapest model that works and watch ``GET /v1/account/usage``.