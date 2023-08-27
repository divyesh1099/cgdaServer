-- Table: gemilms.bill_consignment

-- DROP TABLE gemilms.bill_consignment;

CREATE TABLE gemilms.bill_consignment
(
  gem_invoice_no character varying(100) NOT NULL,
  consignment_ser integer NOT NULL DEFAULT nextval('gemilms.bill_consignment_consignment_serial_no_seq'::regclass),
  consignee_state character varying(50),
  consignee_lastname character varying(100),
  consignee_mobile numeric(15,0),
  consignee_fname character varying(100),
  consignee_pin numeric(10,0),
  consignee_address character varying(255),
  consignee_district character varying(80),
  CONSTRAINT pk_bill_consignment PRIMARY KEY (consignment_ser),
  CONSTRAINT fk_bill_consignment_bill_details FOREIGN KEY (gem_invoice_no)
      REFERENCES gemilms.bill_details (gem_invoice_no) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT unique_gem_invoice_consignee_mobile UNIQUE (gem_invoice_no, consignee_mobile)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE gemilms.bill_consignment
  OWNER TO postgres;
