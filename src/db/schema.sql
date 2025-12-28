CREATE TABLE IF NOT EXISTS extracted_metrics (
  company TEXT NOT NULL,
  report_year INTEGER NOT NULL,
  indicator_name TEXT NOT NULL,
  
  value REAL,
  unit TEXT,
  confidence REAL,
  
  source_page INTEGER,
  source_section TEXT,
  notes TEXT,

  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  PRIMARY KEY (company, report_year, indicator_name)
);