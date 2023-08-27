-- Table: gemilms.bill_consign_products

-- DROP TABLE gemilms.bill_consign_products;

CREATE TABLE gemilms.bill_consign_products
(
  product_code character varying(255) NOT NULL,
  consignment_ser integer NOT NULL DEFAULT nextval('gemilms.bill_consign_products_consignment_serial_no_seq'::regclass),
  product_serial_no integer NOT NULL DEFAULT nextval('gemilms.bill_consign_products_product_serial_no_seq1'::regclass),
  total_value numeric(15,2),
  unit_price numeric(15,2),
  expected_delivery_date timestamp without time zone,
  product_brand character varying(100),
  quantity_ordered numeric(15,2),
  product_name character varying(255),
  sgst numeric(15,2),
  supplied_quantity numeric(15,2),
  freight_sgst numeric(15,2),
  igst numeric(15,2),
  actual_delivery_date timestamp without time zone,
  freight_cgst numeric(15,2),
  hsn_code character varying(20),
  freight_utgst numeric(15,2),
  cgst numeric(15,2),
  cess numeric(15,2),
  freight_igst numeric(15,2),
  freight_cess numeric(15,2),
  utgst numeric(15,2),
  accepted_quantity numeric(15,2),
  frieght_charge numeric(15,2),
  billing_cycle_details_unit character varying(20),
  billing_cycle_details_value integer,
  offering_type character varying(50),
  product_category_id character varying(100),
  product_category_name character varying(100),
  tds_under_gst character varying(20),
  tds_under_incometax character varying(20),
  quantity_unit_type character varying(100),
  CONSTRAINT bill_consign_products_pkey PRIMARY KEY (product_code),
  CONSTRAINT fk_bill_consign_products_bill_consignment FOREIGN KEY (consignment_ser)
      REFERENCES gemilms.bill_consignment (consignment_ser) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE gemilms.bill_consign_products
  OWNER TO postgres;
