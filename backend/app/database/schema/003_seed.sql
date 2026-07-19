--
-- PostgreSQL database dump
--

\restrict EHRL8iD2Nh9Mkzo0gx4JOm1HyMETJ0T7xV267sUcMoYl9hHitrLqu6iTMeHDJbQ

-- Dumped from database version 16.14 (Debian 16.14-1.pgdg13+1)
-- Dumped by pg_dump version 16.14

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: indicators; Type: TABLE DATA; Schema: public; Owner: admin_usr
--

COPY public.indicators (id, name, parameters, description, enabled, priority, created_at) FROM stdin;
1	SMA	20	Simple Moving Average 20	t	10	2026-07-19 18:49:13.065248
2	SMA	50	Simple Moving Average 50	t	20	2026-07-19 18:49:13.065248
3	EMA	20	Exponential Moving Average 20	t	30	2026-07-19 18:49:13.065248
4	EMA	50	Exponential Moving Average 50	t	40	2026-07-19 18:49:13.065248
5	RSI	14	Relative Strength Index	t	50	2026-07-19 18:49:13.065248
6	MACD	12,26,9	Moving Average Convergence Divergence	t	60	2026-07-19 18:49:13.065248
7	BOLLINGER	20,2	Bollinger Bands	t	70	2026-07-19 18:49:13.065248
\.


--
-- Data for Name: monitored_symbols; Type: TABLE DATA; Schema: public; Owner: trading_usr
--

COPY public.monitored_symbols (id, symbol, enabled, interval_seconds, last_execution, provider, priority, last_price) FROM stdin;
2	MSFT	t	300	2026-07-19 22:24:05.951151	Finnhub	100	393.82000000
3	NVDA	t	300	2026-07-19 22:24:06.090166	Finnhub	100	202.81000000
11	GLD	t	300	2026-07-19 22:24:06.231839	Finnhub	100	368.41000000
9	GOOG	t	300	2026-07-19 22:24:06.366063	Finnhub	100	346.12000000
10	HPQ	t	300	2026-07-19 22:24:06.507527	Finnhub	100	24.84000000
8	IBM	t	300	2026-07-19 22:24:06.641148	Finnhub	100	212.67000000
6	INTC	t	300	2026-07-19 22:24:06.774497	Finnhub	100	95.04000000
7	ORCL	t	300	2026-07-19 22:24:06.91034	Finnhub	100	126.41000000
4	QCOM	t	300	2026-07-19 22:24:07.051976	Finnhub	100	171.78000000
12	SLV	t	300	2026-07-19 22:24:07.189466	Finnhub	100	50.78000000
5	STX	t	300	2026-07-19 22:24:07.328223	Finnhub	100	787.66000000
1	AAPL	t	300	2026-07-19 22:24:07.46687	Finnhub	100	333.74000000
\.


--
-- Data for Name: symbol_indicators; Type: TABLE DATA; Schema: public; Owner: admin_usr
--

COPY public.symbol_indicators (symbol, indicator_id, enabled) FROM stdin;
MSFT	1	t
NVDA	1	t
GLD	1	t
GOOG	1	t
HPQ	1	t
IBM	1	t
INTC	1	t
ORCL	1	t
QCOM	1	t
SLV	1	t
STX	1	t
AAPL	1	t
MSFT	2	t
NVDA	2	t
GLD	2	t
GOOG	2	t
HPQ	2	t
IBM	2	t
INTC	2	t
ORCL	2	t
QCOM	2	t
SLV	2	t
STX	2	t
AAPL	2	t
MSFT	3	t
NVDA	3	t
GLD	3	t
GOOG	3	t
HPQ	3	t
IBM	3	t
INTC	3	t
ORCL	3	t
QCOM	3	t
SLV	3	t
STX	3	t
AAPL	3	t
MSFT	4	t
NVDA	4	t
GLD	4	t
GOOG	4	t
HPQ	4	t
IBM	4	t
INTC	4	t
ORCL	4	t
QCOM	4	t
SLV	4	t
STX	4	t
AAPL	4	t
MSFT	5	t
NVDA	5	t
GLD	5	t
GOOG	5	t
HPQ	5	t
IBM	5	t
INTC	5	t
ORCL	5	t
QCOM	5	t
SLV	5	t
STX	5	t
AAPL	5	t
MSFT	6	t
NVDA	6	t
GLD	6	t
GOOG	6	t
HPQ	6	t
IBM	6	t
INTC	6	t
ORCL	6	t
QCOM	6	t
SLV	6	t
STX	6	t
AAPL	6	t
MSFT	7	t
NVDA	7	t
GLD	7	t
GOOG	7	t
HPQ	7	t
IBM	7	t
INTC	7	t
ORCL	7	t
QCOM	7	t
SLV	7	t
STX	7	t
AAPL	7	t
\.


--
-- Name: indicators_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin_usr
--

SELECT pg_catalog.setval('public.indicators_id_seq', 7, true);


--
-- Name: monitored_symbols_id_seq; Type: SEQUENCE SET; Schema: public; Owner: trading_usr
--

SELECT pg_catalog.setval('public.monitored_symbols_id_seq', 12, true);


--
-- PostgreSQL database dump complete
--

\unrestrict EHRL8iD2Nh9Mkzo0gx4JOm1HyMETJ0T7xV267sUcMoYl9hHitrLqu6iTMeHDJbQ

