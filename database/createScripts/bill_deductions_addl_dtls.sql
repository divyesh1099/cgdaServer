-- Table: gemilms.bill_deductions_addl_dtls

-- DROP TABLE gemilms.bill_deductions_addl_dtls;

CREATE TABLE gemilms.bill_deductions_addl_dtls
(
  deduction_serial_no integer NOT NULL,
  additional_details_serial_no serial NOT NULL,
  ld_days integer NOT NULL,
  CONSTRAINT bill_deductions_addl_dtls_pkey PRIMARY KEY (additional_details_serial_no),
  CONSTRAINT fk_bill_deductions FOREIGN KEY (deduction_serial_no)
      REFERENCES gemilms.bill_deductions (deduction_serial_no) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE gemilms.bill_deductions_addl_dtls
  OWNER TO postgres;
