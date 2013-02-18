--
-- PostgreSQL database dump
--

-- Dumped from database version 9.1.8
-- Dumped by pg_dump version 9.1.8
-- Started on 2013-02-18 16:04:20 VET

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- TOC entry 167 (class 3079 OID 11717)
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- TOC entry 1972 (class 0 OID 0)
-- Dependencies: 167
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

--
-- TOC entry 179 (class 1255 OID 3376823)
-- Dependencies: 508 5
-- Name: gen_timestamp(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION gen_timestamp() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
  BEGIN
       IF (NEW.write_date is null) THEN
           NEW.write_date := NOW();
       END IF;
       RETURN NEW;
  END;
$$;


ALTER FUNCTION public.gen_timestamp() OWNER TO postgres;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 163 (class 1259 OID 3376779)
-- Dependencies: 5
-- Name: clients; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE clients (
    id character varying(50) NOT NULL,
    name character varying NOT NULL,
    address character varying NOT NULL,
    phone character varying,
    vat character varying NOT NULL,
    write_date timestamp without time zone NOT NULL
);


ALTER TABLE public.clients OWNER TO postgres;

--
-- TOC entry 165 (class 1259 OID 3376792)
-- Dependencies: 1945 1946 5
-- Name: products; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE products (
    id character varying(50) NOT NULL,
    name character varying NOT NULL,
    quantity integer DEFAULT 0 NOT NULL,
    code character varying NOT NULL,
    price real DEFAULT 0 NOT NULL,
    write_date timestamp without time zone NOT NULL
);


ALTER TABLE public.products OWNER TO postgres;

--
-- TOC entry 164 (class 1259 OID 3376787)
-- Dependencies: 5
-- Name: sales; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE sales (
    id character varying(50) NOT NULL,
    client_id character varying(50) NOT NULL,
    sale_date date NOT NULL,
    write_date timestamp without time zone NOT NULL
);


ALTER TABLE public.sales OWNER TO postgres;

--
-- TOC entry 166 (class 1259 OID 3376802)
-- Dependencies: 1947 5
-- Name: sales_lines; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE sales_lines (
    id character varying(50) NOT NULL,
    sale_id character varying(50) NOT NULL,
    product_id character varying(50) NOT NULL,
    quantity integer DEFAULT 1 NOT NULL,
    write_date timestamp without time zone NOT NULL
);


ALTER TABLE public.sales_lines OWNER TO postgres;

--
-- TOC entry 162 (class 1259 OID 3376770)
-- Dependencies: 5
-- Name: sync_tables; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE sync_tables (
    id integer NOT NULL,
    table_name character varying NOT NULL,
    sync_type character varying NOT NULL,
    order_1 integer NOT NULL
);


ALTER TABLE public.sync_tables OWNER TO postgres;

--
-- TOC entry 161 (class 1259 OID 3376768)
-- Dependencies: 5 162
-- Name: sync_tables_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE sync_tables_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.sync_tables_id_seq OWNER TO postgres;

--
-- TOC entry 1973 (class 0 OID 0)
-- Dependencies: 161
-- Name: sync_tables_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE sync_tables_id_seq OWNED BY sync_tables.id;


--
-- TOC entry 1944 (class 2604 OID 3376773)
-- Dependencies: 162 161 162
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sync_tables ALTER COLUMN id SET DEFAULT nextval('sync_tables_id_seq'::regclass);


--
-- TOC entry 1951 (class 2606 OID 3376786)
-- Dependencies: 163 163 1966
-- Name: client_pk; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY clients
    ADD CONSTRAINT client_pk PRIMARY KEY (id);


--
-- TOC entry 1955 (class 2606 OID 3376801)
-- Dependencies: 165 165 1966
-- Name: product_pk; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY products
    ADD CONSTRAINT product_pk PRIMARY KEY (id);


--
-- TOC entry 1957 (class 2606 OID 3376807)
-- Dependencies: 166 166 1966
-- Name: sale_line_pk; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY sales_lines
    ADD CONSTRAINT sale_line_pk PRIMARY KEY (id);


--
-- TOC entry 1953 (class 2606 OID 3376791)
-- Dependencies: 164 164 1966
-- Name: sale_pk; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY sales
    ADD CONSTRAINT sale_pk PRIMARY KEY (id);


--
-- TOC entry 1949 (class 2606 OID 3376778)
-- Dependencies: 162 162 1966
-- Name: sync_tables_pk; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY sync_tables
    ADD CONSTRAINT sync_tables_pk PRIMARY KEY (id);


--
-- TOC entry 1961 (class 2620 OID 3376825)
-- Dependencies: 179 163 1966
-- Name: ts_clients; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER ts_clients BEFORE INSERT OR UPDATE ON clients FOR EACH ROW EXECUTE PROCEDURE gen_timestamp();


--
-- TOC entry 1963 (class 2620 OID 3376824)
-- Dependencies: 165 179 1966
-- Name: ts_products; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER ts_products BEFORE INSERT OR UPDATE ON products FOR EACH ROW EXECUTE PROCEDURE gen_timestamp();


--
-- TOC entry 1962 (class 2620 OID 3376826)
-- Dependencies: 179 164 1966
-- Name: ts_sales; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER ts_sales BEFORE INSERT OR UPDATE ON sales FOR EACH ROW EXECUTE PROCEDURE gen_timestamp();


--
-- TOC entry 1964 (class 2620 OID 3376829)
-- Dependencies: 166 179 1966
-- Name: ts_sales_lines; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER ts_sales_lines BEFORE INSERT OR UPDATE ON sales_lines FOR EACH ROW EXECUTE PROCEDURE gen_timestamp();


--
-- TOC entry 1958 (class 2606 OID 3376808)
-- Dependencies: 163 1950 164 1966
-- Name: clients_sales_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sales
    ADD CONSTRAINT clients_sales_fk FOREIGN KEY (client_id) REFERENCES clients(id);


--
-- TOC entry 1960 (class 2606 OID 3376818)
-- Dependencies: 1954 165 166 1966
-- Name: products_sales_lines_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sales_lines
    ADD CONSTRAINT products_sales_lines_fk FOREIGN KEY (product_id) REFERENCES products(id);


--
-- TOC entry 1959 (class 2606 OID 3376813)
-- Dependencies: 166 164 1952 1966
-- Name: sales_sales_lines_fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sales_lines
    ADD CONSTRAINT sales_sales_lines_fk FOREIGN KEY (sale_id) REFERENCES sales(id);


--
-- TOC entry 1971 (class 0 OID 0)
-- Dependencies: 5
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


-- Completed on 2013-02-18 16:04:20 VET

--
-- PostgreSQL database dump complete
--

