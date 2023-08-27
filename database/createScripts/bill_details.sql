-- Table: gemilms.bill_details

-- DROP TABLE gemilms.bill_details;

CREATE TABLE gemilms.bill_details
(
  gem_invoice_no character varying(100) NOT NULL,
  buyer_address character varying(255),
  buyer_district character varying(80),
  buyer_email character varying(100),
  buyer_gstn character varying(30),
  buyer_mobile numeric(15,0),
  buyer_name character varying(100),
  buyer_org character varying(255),
  buyer_pincode numeric(10,0),
  buyer_state character varying(50),
  demand_id character varying(100),
  designation_financial character varying(50),
  ifd_concurrance integer,
  ifd_diary_date timestamp without time zone,
  ifd_diary_no character varying(50),
  order_amount numeric(15,2),
  order_date timestamp without time zone NOT NULL,
  order_id character varying(255) NOT NULL,
  seller_id character varying(255),
  supply_order_date timestamp without time zone,
  supply_order_no character varying(255),
  vendor_address character varying(255),
  vendor_bank_account_no character varying(100),
  vendor_bank_ifsc_code character varying(15),
  vendor_code character varying(50),
  vendor_district character varying(80),
  vendor_gstn character varying(30),
  vendor_name character varying(255),
  vendor_pan character varying(12),
  vendor_pin numeric(10,0),
  vendor_state character varying(50),
  bill_no character varying(50),
  bill_date timestamp without time zone,
  bill_amount numeric(15,2),
  fa_file character varying(255),
  crac_file character varying(255),
  contract_file character varying(255),
  receipt_no character varying(100),
  receipt_date timestamp without time zone,
  crac_date timestamp without time zone,
  bill_file character varying(255),
  invoice_file character varying(255),
  invoice_date timestamp without time zone,
  invoice_no character varying(255),
  pg_mode character varying(10),
  request_ser integer NOT NULL,
  response_ser integer,
  createddatetime timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
  syncdatetime timestamp without time zone,
  vendor_gst_status character varying(255),
  vendor_unique_id character varying(10),
  create_on timestamp without time zone,
  transaction_id numeric(40,0),
  CONSTRAINT pk_bill_details PRIMARY KEY (gem_invoice_no)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE gemilms.bill_details
  OWNER TO postgres;
