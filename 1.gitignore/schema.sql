--
-- PostgreSQL database dump
--

-- Dumped from database version 12.22 (Ubuntu 12.22-0ubuntu0.20.04.1)
-- Dumped by pg_dump version 12.22 (Ubuntu 12.22-0ubuntu0.20.04.1)

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
-- Name: audit_logs; Type: TABLE; Schema: public; Owner: permit_user
--

CREATE TABLE public.audit_logs (
    id integer NOT NULL,
    permit_id integer NOT NULL,
    action character varying(50) NOT NULL,
    admin_id integer NOT NULL,
    "timestamp" timestamp without time zone NOT NULL,
    reason character varying(255)
);


ALTER TABLE public.audit_logs OWNER TO permit_user;

--
-- Name: audit_logs_id_seq; Type: SEQUENCE; Schema: public; Owner: permit_user
--

CREATE SEQUENCE public.audit_logs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.audit_logs_id_seq OWNER TO permit_user;

--
-- Name: audit_logs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: permit_user
--

ALTER SEQUENCE public.audit_logs_id_seq OWNED BY public.audit_logs.id;


--
-- Name: mutare_submission; Type: TABLE; Schema: public; Owner: permit_user
--

CREATE TABLE public.mutare_submission (
    id integer NOT NULL,
    status character varying(255)
);


ALTER TABLE public.mutare_submission OWNER TO permit_user;

--
-- Name: mutare_submission_id_seq; Type: SEQUENCE; Schema: public; Owner: permit_user
--

CREATE SEQUENCE public.mutare_submission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mutare_submission_id_seq OWNER TO permit_user;

--
-- Name: mutare_submission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: permit_user
--

ALTER SEQUENCE public.mutare_submission_id_seq OWNED BY public.mutare_submission.id;


--
-- Name: permit; Type: TABLE; Schema: public; Owner: permit_user
--

CREATE TABLE public.permit (
    salutation character varying(10) NOT NULL,
    name character varying(100) NOT NULL,
    address character varying(200) NOT NULL,
    number_of_animals integer NOT NULL,
    animal_type character varying(50) NOT NULL,
    cattle_type character varying(50),
    other_animal_type character varying(100),
    origin character varying(100) NOT NULL,
    origin_district character varying(100) NOT NULL,
    destination character varying(100) NOT NULL,
    destination_district character varying(100) NOT NULL,
    movement_period integer NOT NULL,
    route character varying(200) NOT NULL,
    payment_amount double precision NOT NULL,
    payment_amount_in_words character varying(200) NOT NULL,
    date timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    status character varying(50) DEFAULT 'Submitted'::character varying,
    id integer NOT NULL,
    origin_status character varying(20) DEFAULT 'Pending'::character varying,
    destination_status character varying(20) DEFAULT 'Pending'::character varying
);


ALTER TABLE public.permit OWNER TO permit_user;

--
-- Name: permit_id_seq; Type: SEQUENCE; Schema: public; Owner: permit_user
--

CREATE SEQUENCE public.permit_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.permit_id_seq OWNER TO permit_user;

--
-- Name: permit_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: permit_user
--

ALTER SEQUENCE public.permit_id_seq OWNED BY public.permit.id;


--
-- Name: audit_logs id; Type: DEFAULT; Schema: public; Owner: permit_user
--

ALTER TABLE ONLY public.audit_logs ALTER COLUMN id SET DEFAULT nextval('public.audit_logs_id_seq'::regclass);


--
-- Name: mutare_submission id; Type: DEFAULT; Schema: public; Owner: permit_user
--

ALTER TABLE ONLY public.mutare_submission ALTER COLUMN id SET DEFAULT nextval('public.mutare_submission_id_seq'::regclass);


--
-- Name: permit id; Type: DEFAULT; Schema: public; Owner: permit_user
--

ALTER TABLE ONLY public.permit ALTER COLUMN id SET DEFAULT nextval('public.permit_id_seq'::regclass);


--
-- Name: audit_logs audit_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: permit_user
--

ALTER TABLE ONLY public.audit_logs
    ADD CONSTRAINT audit_logs_pkey PRIMARY KEY (id);


--
-- Name: mutare_submission mutare_submission_pkey; Type: CONSTRAINT; Schema: public; Owner: permit_user
--

ALTER TABLE ONLY public.mutare_submission
    ADD CONSTRAINT mutare_submission_pkey PRIMARY KEY (id);


--
-- Name: permit permit_pkey; Type: CONSTRAINT; Schema: public; Owner: permit_user
--

ALTER TABLE ONLY public.permit
    ADD CONSTRAINT permit_pkey PRIMARY KEY (id);


--
-- Name: audit_logs audit_logs_permit_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: permit_user
--

ALTER TABLE ONLY public.audit_logs
    ADD CONSTRAINT audit_logs_permit_id_fkey FOREIGN KEY (permit_id) REFERENCES public.permit(id);


--
-- PostgreSQL database dump complete
--

