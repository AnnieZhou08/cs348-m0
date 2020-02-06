-- DROP TABLE IF EXISTS Reviews ;
CREATE TABLE IF NOT EXISTS Reviews (
  listing_id INT,
  review_id INT,
  date DATE,
  user_id INT,
  comments VARCHAR(1000),
  PRIMARY KEY (review_id)
);
