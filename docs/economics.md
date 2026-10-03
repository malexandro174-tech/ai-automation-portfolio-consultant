# Economics summary

Forecast от 2 октября 2026, не invoice и не measured ROI. 20 public запросов: mean input 1789, output 116.45 tokens; answer cache выключен. Внешний observed model — deepseek-flash. Planning rate: $0.30/M cache-miss input и $1.20/M output; источник и дата: [DeepSeek pricing](https://api-docs.deepseek.com/quick_start/pricing/), 2026-10-02. Provider prefix cache не принят как гарантированная экономия.

Формула LLM: requests × (1789 × 0.30 + 116.45 × 1.20) / 1_000_000 × 1.05. Далее +$12/month allocated infrastructure ($7 app/DB/backups, $5 shared BGE compute), +$50/month support (2 ч × $25), затем 20% operating buffer. Это допущения, не фактические счета; BGE reuse не делает compute бесплатным.

| Запросов / месяц | LLM USD с retry allowance | Месяц целиком USD | Первый год USD |
|---|---|---|---|
| 500 | 0.36 | 74.83 | 1797.91 |
| 3000 | 2.13 | 76.96 | 1823.48 |
| 10000 | 7.10 | 82.92 | 1895.08 |

Первый год включает плановый setup $900: 30 часов × $25 +20%; это не измеренные labor hours. Public consultant бесплатен посетителю, будущий managed deployment требует отдельного обследования. ROI, CAC/LTV, conversion и usefulness pilot пока не измерены. Перед новым коммерческим расчётом тарифы и allocation нужно проверить заново.
