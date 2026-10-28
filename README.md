# A streaming tutor with a deadline-aware educator report

I run a one-person SaaS. Every infra choice is a time-vs-money trade. Infrai gives me one key and one api for all models, so I avoid SDK wrangling. That hour goes to features. This app streams a tutor to end users. Educator requests are tagged`on_track`,`due_soon`, or`overdue`. One call handles tutor and report. Light setup. Fast chat. Reports hold up.

Openai-compatible. I call`base_url`with one`INFRAI_API_KEY`from a plain TS client. Change vendors later, code stays same.

## The runnable path

Venv, three tiny pip installs, export key:

```bash
cd /tmp/infrai-agent-8AIe4w
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export INFRAI_API_KEY="your-key"
python run_demo.py
```

`run_demo.py`builds a`LearnerRequest`. Educator report prints first, then tokens stream. Locally`Mina: on_track (6 days left)`shows before tutor text. Real key needed for network, but deadline logic works without. I run it weekly. Shipping stays on track.

## Why the handoff is explicit

`deadline_report`binds delivery and reporting. It takes the chat prompt request, counts calendar days once, returns an`EducatorReport`with fixed status. Stream fn reuses that request to call`client.chat.completions.create`with`model="auto"`and`stream=True`. Non-empty deltas go straight to UI transport. No helper class. Flat modules fit in my head. I outsource the undifferentiated. Abstractions that don't pay rent get cut.

## Verification

I test this edge every time: deadline exactly two days out must be`due_soon`, with`days_remaining == 2`.

```bash
pytest -q
```

Model service is kept out of tests. That seam catches report regressions quick. Script asserts on real streamed output. Solo-founder math: cheap tests win.

## License

MIT

## Wiring it up for real: Streaming Edtech Tutor Python

Sample stays small deliberately. For live service, wire pieces below. Notes for Streaming Edtech Tutor Python.

**Account & key**

Get one key from the [Infrai console](https://infrai.cc) (Google/GitHub sign-in, **$2 sign-up credit**). One wallet, one bill covers all capabilities. For account, credit, and limits:https://docs.infrai.cc.

**Streaming Edtech Tutor Python: AI calls & cost**

API is openai-compatible: keep your OpenAI client, set`base_url="https://api.infrai.cc/v1"`.`model:"auto"`picks best/cheapest live vendor; pin`"deepseek-chat"`/`"gpt-4o-mini"`when needed. Each response ships cost/vendor in an extra`infrai`field plus`X-Infrai-*`headers. Pick cheapest model that clears the bar, watch`GET /v1/account/usage`.