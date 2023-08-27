-- Table: gemilms.bill_deductions

-- DROP TABLE gemilms.bill_deductions;

CREATE TABLE gemilms.bill_deductions
(
  gem_invoice_no character varying(100) NOT NULL,
  deduction_serial_no serial NOT NULL,
  dedn_reason text,
  dedn_amount double precision,
  dedn_name character varying(150),
  dedn_type character varying(150),
  CONSTRAINT bill_deductions_pkey PRIMARY KEY (deduction_serial_no),
  CONSTRAINT fk_bill_details FOREIGN KEY (gem_invoice_no)
      REFERENCES gemilms.bill_details (gem_invoice_no) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT unique_bill_deductions UNIQUE (gem_invoice_no, dedn_name, dedn_type)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE gemilms.bill_deductions
  OWNER TO postgres;
