--
-- PostgreSQL database dump
--

\restrict dthLBqhoit226oRpRMLeEYJu1RJkVZk2sjCgLMu3cLtbWz5O1QY3KY6MlIJ856C

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

SET default_table_access_method = heap;

--
-- Name: database_info; Type: TABLE; Schema: public; Owner: admin_usr
--

CREATE TABLE public.database_info (
    id integer NOT NULL,
    version character varying(20) NOT NULL,
    initialized_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.database_info OWNER TO admin_usr;

--
-- Name: database_info_id_seq; Type: SEQUENCE; Schema: public; Owner: admin_usr
--

CREATE SEQUENCE public.database_info_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.database_info_id_seq OWNER TO admin_usr;

--
-- Name: database_info_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin_usr
--

ALTER SEQUENCE public.database_info_id_seq OWNED BY public.database_info.id;


--
-- Name: indicator_values; Type: TABLE; Schema: public; Owner: admin_usr
--

CREATE TABLE public.indicator_values (
    id integer NOT NULL,
    symbol character varying(20) NOT NULL,
    indicator character varying(50) NOT NULL,
    parameters character varying(20) NOT NULL,
    quote_time timestamp without time zone NOT NULL,
    value1 numeric(18,8),
    value2 numeric(18,8),
    value3 numeric(18,8),
    created_at timestamp without time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.indicator_values OWNER TO admin_usr;

--
-- Name: indicator_values_id_seq; Type: SEQUENCE; Schema: public; Owner: admin_usr
--

CREATE SEQUENCE public.indicator_values_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.indicator_values_id_seq OWNER TO admin_usr;

--
-- Name: indicator_values_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin_usr
--

ALTER SEQUENCE public.indicator_values_id_seq OWNED BY public.indicator_values.id;


--
-- Name: indicators; Type: TABLE; Schema: public; Owner: admin_usr
--

CREATE TABLE public.indicators (
    id integer NOT NULL,
    name character varying(30) NOT NULL,
    parameters character varying(50) NOT NULL,
    description character varying(200),
    enabled boolean DEFAULT true NOT NULL,
    priority integer DEFAULT 100 NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.indicators OWNER TO admin_usr;

--
-- Name: indicators_id_seq; Type: SEQUENCE; Schema: public; Owner: admin_usr
--

CREATE SEQUENCE public.indicators_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.indicators_id_seq OWNER TO admin_usr;

--
-- Name: indicators_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin_usr
--

ALTER SEQUENCE public.indicators_id_seq OWNED BY public.indicators.id;


--
-- Name: market_quotes; Type: TABLE; Schema: public; Owner: trading_usr
--

CREATE TABLE public.market_quotes (
    id bigint NOT NULL,
    symbol character varying(20) NOT NULL,
    quote_time timestamp with time zone NOT NULL,
    price numeric(18,6) NOT NULL,
    change_value numeric(18,6),
    change_percent numeric(10,6),
    day_high numeric(18,6),
    day_low numeric(18,6),
    day_open numeric(18,6),
    previous_close numeric(18,6),
    source character varying(50) DEFAULT 'FINNHUB'::character varying,
    created_at timestamp with time zone DEFAULT CURRENT_TIMESTAMP,
    provider_quote_time timestamp without time zone
);


ALTER TABLE public.market_quotes OWNER TO trading_usr;

--
-- Name: market_quotes_id_seq; Type: SEQUENCE; Schema: public; Owner: trading_usr
--

CREATE SEQUENCE public.market_quotes_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.market_quotes_id_seq OWNER TO trading_usr;

--
-- Name: market_quotes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: trading_usr
--

ALTER SEQUENCE public.market_quotes_id_seq OWNED BY public.market_quotes.id;


--
-- Name: monitored_symbols; Type: TABLE; Schema: public; Owner: trading_usr
--

CREATE TABLE public.monitored_symbols (
    id integer NOT NULL,
    symbol character varying(20),
    enabled boolean DEFAULT true,
    interval_seconds integer DEFAULT 300 NOT NULL,
    last_execution timestamp without time zone,
    provider character varying(50) DEFAULT 'Finnhub'::character varying NOT NULL,
    priority integer DEFAULT 100 NOT NULL,
    last_price numeric(18,8)
);


ALTER TABLE public.monitored_symbols OWNER TO trading_usr;

--
-- Name: monitored_symbols_id_seq; Type: SEQUENCE; Schema: public; Owner: trading_usr
--

CREATE SEQUENCE public.monitored_symbols_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.monitored_symbols_id_seq OWNER TO trading_usr;

--
-- Name: monitored_symbols_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: trading_usr
--

ALTER SEQUENCE public.monitored_symbols_id_seq OWNED BY public.monitored_symbols.id;


--
-- Name: symbol_indicators; Type: TABLE; Schema: public; Owner: admin_usr
--

CREATE TABLE public.symbol_indicators (
    symbol character varying(20) NOT NULL,
    indicator_id integer NOT NULL,
    enabled boolean DEFAULT true NOT NULL
);


ALTER TABLE public.symbol_indicators OWNER TO admin_usr;

--
-- Name: trading_log; Type: TABLE; Schema: public; Owner: trading_usr
--

CREATE TABLE public.trading_log (
    id integer NOT NULL,
    startup_time timestamp without time zone NOT NULL
);


ALTER TABLE public.trading_log OWNER TO trading_usr;

--
-- Name: trading_log_id_seq; Type: SEQUENCE; Schema: public; Owner: trading_usr
--

CREATE SEQUENCE public.trading_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.trading_log_id_seq OWNER TO trading_usr;

--
-- Name: trading_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: trading_usr
--

ALTER SEQUENCE public.trading_log_id_seq OWNED BY public.trading_log.id;


--
-- Name: database_info id; Type: DEFAULT; Schema: public; Owner: admin_usr
--

ALTER TABLE ONLY public.database_info ALTER COLUMN id SET DEFAULT nextval('public.database_info_id_seq'::regclass);


--
-- Name: indicator_values id; Type: DEFAULT; Schema: public; Owner: admin_usr
--

ALTER TABLE ONLY public.indicator_values ALTER COLUMN id SET DEFAULT nextval('public.indicator_values_id_seq'::regclass);


--
-- Name: indicators id; Type: DEFAULT; Schema: public; Owner: admin_usr
--

ALTER TABLE ONLY public.indicators ALTER COLUMN id SET DEFAULT nextval('public.indicators_id_seq'::regclass);


--
-- Name: market_quotes id; Type: DEFAULT; Schema: public; Owner: trading_usr
--

ALTER TABLE ONLY public.market_quotes ALTER COLUMN id SET DEFAULT nextval('public.market_quotes_id_seq'::regclass);


--
-- Name: monitored_symbols id; Type: DEFAULT; Schema: public; Owner: trading_usr
--

ALTER TABLE ONLY public.monitored_symbols ALTER COLUMN id SET DEFAULT nextval('public.monitored_symbols_id_seq'::regclass);


--
-- Name: trading_log id; Type: DEFAULT; Schema: public; Owner: trading_usr
--

ALTER TABLE ONLY public.trading_log ALTER COLUMN id SET DEFAULT nextval('public.trading_log_id_seq'::regclass);


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: pg_database_owner
--

GRANT ALL ON SCHEMA public TO trading_usr;


--
-- Name: TABLE database_info; Type: ACL; Schema: public; Owner: admin_usr
--

GRANT ALL ON TABLE public.database_info TO trading_usr;


--
-- Name: SEQUENCE database_info_id_seq; Type: ACL; Schema: public; Owner: admin_usr
--

GRANT ALL ON SEQUENCE public.database_info_id_seq TO trading_usr;


--
-- Name: TABLE indicator_values; Type: ACL; Schema: public; Owner: admin_usr
--

GRANT ALL ON TABLE public.indicator_values TO trading_usr;


--
-- Name: SEQUENCE indicator_values_id_seq; Type: ACL; Schema: public; Owner: admin_usr
--

GRANT ALL ON SEQUENCE public.indicator_values_id_seq TO trading_usr;


--
-- Name: TABLE indicators; Type: ACL; Schema: public; Owner: admin_usr
--

GRANT ALL ON TABLE public.indicators TO trading_usr;


--
-- Name: SEQUENCE indicators_id_seq; Type: ACL; Schema: public; Owner: admin_usr
--

GRANT ALL ON SEQUENCE public.indicators_id_seq TO trading_usr;


--
-- Name: TABLE symbol_indicators; Type: ACL; Schema: public; Owner: admin_usr
--

GRANT ALL ON TABLE public.symbol_indicators TO trading_usr;


--
-- PostgreSQL database dump complete
--

\unrestrict dthLBqhoit226oRpRMLeEYJu1RJkVZk2sjCgLMu3cLtbWz5O1QY3KY6MlIJ856C

