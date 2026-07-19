--
-- PostgreSQL database dump
--

\restrict MW8yrrfOoIlZnKe5txRvS3fLjq9jhfQmtwWGLEFFShhV0kcjTSAqbQqPbcsjddU

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

SET default_tablespace = '';

--
-- Name: database_info database_info_pkey; Type: CONSTRAINT; Schema: public; Owner: admin_usr
--

ALTER TABLE ONLY public.database_info
    ADD CONSTRAINT database_info_pkey PRIMARY KEY (id);


--
-- Name: indicator_values indicator_values_pkey; Type: CONSTRAINT; Schema: public; Owner: admin_usr
--

ALTER TABLE ONLY public.indicator_values
    ADD CONSTRAINT indicator_values_pkey PRIMARY KEY (id);


--
-- Name: indicators indicators_pkey; Type: CONSTRAINT; Schema: public; Owner: admin_usr
--

ALTER TABLE ONLY public.indicators
    ADD CONSTRAINT indicators_pkey PRIMARY KEY (id);


--
-- Name: market_quotes market_quotes_pkey; Type: CONSTRAINT; Schema: public; Owner: trading_usr
--

ALTER TABLE ONLY public.market_quotes
    ADD CONSTRAINT market_quotes_pkey PRIMARY KEY (id);


--
-- Name: monitored_symbols monitored_symbols_pkey; Type: CONSTRAINT; Schema: public; Owner: trading_usr
--

ALTER TABLE ONLY public.monitored_symbols
    ADD CONSTRAINT monitored_symbols_pkey PRIMARY KEY (id);


--
-- Name: monitored_symbols monitored_symbols_symbol_key; Type: CONSTRAINT; Schema: public; Owner: trading_usr
--

ALTER TABLE ONLY public.monitored_symbols
    ADD CONSTRAINT monitored_symbols_symbol_key UNIQUE (symbol);


--
-- Name: symbol_indicators symbol_indicators_pkey; Type: CONSTRAINT; Schema: public; Owner: admin_usr
--

ALTER TABLE ONLY public.symbol_indicators
    ADD CONSTRAINT symbol_indicators_pkey PRIMARY KEY (symbol, indicator_id);


--
-- Name: trading_log trading_log_pkey; Type: CONSTRAINT; Schema: public; Owner: trading_usr
--

ALTER TABLE ONLY public.trading_log
    ADD CONSTRAINT trading_log_pkey PRIMARY KEY (id);


--
-- Name: indicator_values uk_indicator_values; Type: CONSTRAINT; Schema: public; Owner: admin_usr
--

ALTER TABLE ONLY public.indicator_values
    ADD CONSTRAINT uk_indicator_values UNIQUE (symbol, indicator, parameters, quote_time);


--
-- Name: idx_indicators_priority; Type: INDEX; Schema: public; Owner: admin_usr
--

CREATE INDEX idx_indicators_priority ON public.indicators USING btree (priority);


--
-- Name: idx_market_quotes_symbol_time; Type: INDEX; Schema: public; Owner: trading_usr
--

CREATE INDEX idx_market_quotes_symbol_time ON public.market_quotes USING btree (symbol, quote_time DESC);


--
-- Name: idx_symbol_indicators_enabled; Type: INDEX; Schema: public; Owner: admin_usr
--

CREATE INDEX idx_symbol_indicators_enabled ON public.symbol_indicators USING btree (enabled);


--
-- Name: idx_symbols_enabled; Type: INDEX; Schema: public; Owner: trading_usr
--

CREATE INDEX idx_symbols_enabled ON public.monitored_symbols USING btree (enabled);


--
-- Name: idx_symbols_execution; Type: INDEX; Schema: public; Owner: trading_usr
--

CREATE INDEX idx_symbols_execution ON public.monitored_symbols USING btree (enabled, last_execution);


--
-- Name: symbol_indicators fk_symbol_indicators_indicator; Type: FK CONSTRAINT; Schema: public; Owner: admin_usr
--

ALTER TABLE ONLY public.symbol_indicators
    ADD CONSTRAINT fk_symbol_indicators_indicator FOREIGN KEY (indicator_id) REFERENCES public.indicators(id) ON DELETE CASCADE;


--
-- Name: symbol_indicators fk_symbol_indicators_symbol; Type: FK CONSTRAINT; Schema: public; Owner: admin_usr
--

ALTER TABLE ONLY public.symbol_indicators
    ADD CONSTRAINT fk_symbol_indicators_symbol FOREIGN KEY (symbol) REFERENCES public.monitored_symbols(symbol) ON DELETE CASCADE;


--
-- Name: DEFAULT PRIVILEGES FOR SEQUENCES; Type: DEFAULT ACL; Schema: public; Owner: admin_usr
--

ALTER DEFAULT PRIVILEGES FOR ROLE admin_usr IN SCHEMA public GRANT ALL ON SEQUENCES TO trading_usr;


--
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: public; Owner: admin_usr
--

ALTER DEFAULT PRIVILEGES FOR ROLE admin_usr IN SCHEMA public GRANT ALL ON TABLES TO trading_usr;


--
-- PostgreSQL database dump complete
--

\unrestrict MW8yrrfOoIlZnKe5txRvS3fLjq9jhfQmtwWGLEFFShhV0kcjTSAqbQqPbcsjddU

