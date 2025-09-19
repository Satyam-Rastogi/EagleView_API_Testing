# EagleView Reports Information

## Where Reports Are Saved

When using the EagleView API client programs, reports and their associated files are saved in the following locations:

### 1. Report Metadata (JSON Files)
- **Location:** Root directory (where the program is run)
- **Files Created:**
  - `eagleview_reports_client_credentials_*.csv` - Summary of all reports in CSV format
  - `eagleview_reports_client_credentials_*.json` - Detailed report data in JSON format
  - Individual report detail files: `report_{report_id}_detail.json`

### 2. Downloaded Report Files
- **Location:** `downloaded_reports/` directory
- **Files Created:**
  - PDF reports: `report_{report_id}.pdf`
  - ZIP deliverables: `report_{report_id}_file_{n}_ZIP.zip`
  - Other file types based on report configuration

### 3. Download Summary
- **Location:** Root directory
- **File:** `downloaded_reports_summary_*.json` - Summary of all downloaded files with metadata

## EC Premium Reports

EC Premium Reports are standard measurement/order reports in the EagleView system. They can be identified by:
- Product type information in the report metadata
- Enhanced measurement data and analysis
- Additional deliverables compared to basic reports

### How to Download EC Premium Reports

1. **Fetch All Reports:**
   The `fetch_and_download_reports.py` program automatically retrieves all reports for the authenticated customer, including EC Premium Reports.

2. **Identify EC Premium Reports:**
   In the report metadata, look for:
   - Product name containing "Premium" or "EC"
   - Enhanced measurement fields
   - Additional file deliverables

3. **Download Report Files:**
   The program automatically:
   - Gets detailed report information
   - Retrieves file download links
   - Downloads all available files for each report
   - Saves files with descriptive names

### Report File Types

EC Premium Reports typically include:
1. **PDF Report:** Main report document with measurements and analysis
2. **ZIP Deliverables:** Additional files such as:
   - Measurement data files
   - Image files
   - CAD files
   - Other product-specific deliverables

### Accessing Downloaded Reports

After running the `fetch_and_download_reports.py` program:
1. Check the `downloaded_reports/` directory for PDF and ZIP files
2. Review the `downloaded_reports_summary_*.json` file for a complete list of downloaded files
3. Examine individual `report_{report_id}_detail.json` files for report metadata

### Example Report Data Structure

```json
{
  "Id": "123456",
  "Status": "Complete",
  "ProductPrimary": "EC Premium Report",
  "DatePlaced": "2025-09-20T10:30:00Z",
  "DateCompleted": "2025-09-20T11:45:00Z",
  "ReportDownloadLink": "https://apicenter.eagleview.com/v1/File/GetReportFile?...",
  "Area": "2450 sq ft",
  "Pitch": "6/12"
}
```

The `ReportDownloadLink` field provides direct access to download the main PDF report.