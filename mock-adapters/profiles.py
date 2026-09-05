"""Deterministic demo profiles shared by all mock verification sources.

These records intentionally resemble normalized data a production adapter would
return after translating a source-specific government-portal response.
"""

from copy import deepcopy


PROFILES = {
    "BIDDER-ALPHA": {
        "display_name": "Aarohan Office Systems Private Limited",
        "scenario": "fully_compliant",
        "udyam": {
            "status": "compliant",
            "last_updated": "2026-08-29T10:15:00Z",
            "confidence": 0.98,
            "raw_fields": {
                "udyam_registration_number": "UDYAM-DL-05-0012345",
                "enterprise_name": "Aarohan Office Systems Private Limited",
                "registration_valid_until": "2029-03-31",
                "enterprise_category": "Small",
                "registration_active": True,
            },
        },
        "gstn": {
            "status": "compliant",
            "last_updated": "2026-08-31T18:00:00Z",
            "confidence": 0.99,
            "raw_fields": {
                "gstin": "07AABCA1234A1Z5",
                "legal_name": "Aarohan Office Systems Private Limited",
                "registration_status": "Active",
                "latest_return_period": "2026-07",
                "latest_return_filed": True,
                "filing_status": "Regular",
            },
        },
        "pan_it": {
            "status": "compliant",
            "last_updated": "2026-08-24T09:30:00Z",
            "confidence": 0.97,
            "raw_fields": {
                "pan": "AABCA1234A",
                "pan_status": "Active",
                "name_match": True,
                "income_tax_return_assessment_year": "2025-26",
                "income_tax_return_filed": True,
            },
        },
        "epfo_esic": {
            "status": "compliant",
            "last_updated": "2026-08-28T14:45:00Z",
            "confidence": 0.95,
            "raw_fields": {
                "epfo_establishment_id": "DLCPM1234567000",
                "epfo_contribution_status": "Paid",
                "esic_employer_code": "11001234560000999",
                "esic_contribution_status": "Paid",
                "latest_contribution_period": "2026-07",
            },
        },
        "digilocker": {
            "status": "compliant",
            "last_updated": "2026-08-30T12:20:00Z",
            "confidence": 0.96,
            "raw_fields": {
                "consent_status": "Granted",
                "identity_document_verified": True,
                "authorized_signatory_verified": True,
                "credential_issued_at": "2026-08-30T12:18:00Z",
            },
        },
        "blacklist": {
            "status": "compliant",
            "last_updated": "2026-09-01T06:00:00Z",
            "confidence": 0.93,
            "raw_fields": {
                "registry_match": False,
                "debarment_status": "Not listed",
                "registry_search_reference": "BLR-20260901-001",
            },
        },
    },
    "BIDDER-BRAVO": {
        "display_name": "Bharat Supplies and Services LLP",
        "scenario": "missing_gst_filing",
        "udyam": {
            "status": "compliant", "last_updated": "2026-08-20T11:00:00Z", "confidence": 0.97,
            "raw_fields": {"udyam_registration_number": "UDYAM-MH-19-0087654", "enterprise_name": "Bharat Supplies and Services LLP", "registration_valid_until": "2028-09-30", "enterprise_category": "Medium", "registration_active": True},
        },
        "gstn": {
            "status": "non_compliant", "last_updated": "2026-08-31T18:00:00Z", "confidence": 0.99,
            "raw_fields": {"gstin": "27AACFB5678K1Z2", "legal_name": "Bharat Supplies and Services LLP", "registration_status": "Active", "latest_return_period": "2026-07", "latest_return_filed": False, "filing_status": "Return overdue", "overdue_return_periods": ["2026-06", "2026-07"]},
        },
        "pan_it": {
            "status": "compliant", "last_updated": "2026-08-22T10:10:00Z", "confidence": 0.96,
            "raw_fields": {"pan": "AACFB5678K", "pan_status": "Active", "name_match": True, "income_tax_return_assessment_year": "2025-26", "income_tax_return_filed": True},
        },
        "epfo_esic": {
            "status": "compliant", "last_updated": "2026-08-27T13:00:00Z", "confidence": 0.94,
            "raw_fields": {"epfo_establishment_id": "MHBAN7654321000", "epfo_contribution_status": "Paid", "esic_employer_code": "31000987650000123", "esic_contribution_status": "Paid", "latest_contribution_period": "2026-07"},
        },
        "digilocker": {
            "status": "compliant", "last_updated": "2026-08-30T09:00:00Z", "confidence": 0.95,
            "raw_fields": {"consent_status": "Granted", "identity_document_verified": True, "authorized_signatory_verified": True, "credential_issued_at": "2026-08-30T08:59:00Z"},
        },
        "blacklist": {
            "status": "compliant", "last_updated": "2026-09-01T06:00:00Z", "confidence": 0.93,
            "raw_fields": {"registry_match": False, "debarment_status": "Not listed", "registry_search_reference": "BLR-20260901-002"},
        },
    },
    "BIDDER-CHARLIE": {
        "display_name": "Crestline Engineering Works",
        "scenario": "blacklisted",
        "udyam": {
            "status": "compliant", "last_updated": "2026-08-21T11:00:00Z", "confidence": 0.97,
            "raw_fields": {"udyam_registration_number": "UDYAM-KA-29-0043210", "enterprise_name": "Crestline Engineering Works", "registration_valid_until": "2028-12-31", "enterprise_category": "Small", "registration_active": True},
        },
        "gstn": {
            "status": "compliant", "last_updated": "2026-08-31T18:00:00Z", "confidence": 0.98,
            "raw_fields": {"gstin": "29AACFC9012P1Z8", "legal_name": "Crestline Engineering Works", "registration_status": "Active", "latest_return_period": "2026-07", "latest_return_filed": True, "filing_status": "Regular"},
        },
        "pan_it": {
            "status": "compliant", "last_updated": "2026-08-25T09:00:00Z", "confidence": 0.96,
            "raw_fields": {"pan": "AACFC9012P", "pan_status": "Active", "name_match": True, "income_tax_return_assessment_year": "2025-26", "income_tax_return_filed": True},
        },
        "epfo_esic": {
            "status": "compliant", "last_updated": "2026-08-28T12:00:00Z", "confidence": 0.94,
            "raw_fields": {"epfo_establishment_id": "KABAN1357911000", "epfo_contribution_status": "Paid", "esic_employer_code": "49000135790000456", "esic_contribution_status": "Paid", "latest_contribution_period": "2026-07"},
        },
        "digilocker": {
            "status": "compliant", "last_updated": "2026-08-30T10:00:00Z", "confidence": 0.96,
            "raw_fields": {"consent_status": "Granted", "identity_document_verified": True, "authorized_signatory_verified": True, "credential_issued_at": "2026-08-30T09:58:00Z"},
        },
        "blacklist": {
            "status": "non_compliant", "last_updated": "2026-09-01T06:00:00Z", "confidence": 0.99,
            "raw_fields": {"registry_match": True, "debarment_status": "Debarred", "debarment_authority": "Mock Central Procurement Registry", "debarment_reason": "Material breach of prior contract", "debarment_until": "2027-06-30", "registry_search_reference": "BLR-20260901-003"},
        },
    },
    "BIDDER-DELTA": {
        "display_name": "Disha Digital Solutions Private Limited",
        "scenario": "expired_udyam",
        "udyam": {
            "status": "expired", "last_updated": "2026-08-15T11:00:00Z", "confidence": 0.98,
            "raw_fields": {"udyam_registration_number": "UDYAM-UP-09-0076543", "enterprise_name": "Disha Digital Solutions Private Limited", "registration_valid_until": "2026-06-30", "enterprise_category": "Small", "registration_active": False},
        },
        "gstn": {
            "status": "compliant", "last_updated": "2026-08-31T18:00:00Z", "confidence": 0.98,
            "raw_fields": {"gstin": "09AACCD3456R1Z4", "legal_name": "Disha Digital Solutions Private Limited", "registration_status": "Active", "latest_return_period": "2026-07", "latest_return_filed": True, "filing_status": "Regular"},
        },
        "pan_it": {
            "status": "compliant", "last_updated": "2026-08-23T10:00:00Z", "confidence": 0.97,
            "raw_fields": {"pan": "AACCD3456R", "pan_status": "Active", "name_match": True, "income_tax_return_assessment_year": "2025-26", "income_tax_return_filed": True},
        },
        "epfo_esic": {
            "status": "compliant", "last_updated": "2026-08-28T12:00:00Z", "confidence": 0.94,
            "raw_fields": {"epfo_establishment_id": "UPKAN2468135000", "epfo_contribution_status": "Paid", "esic_employer_code": "67000246810000789", "esic_contribution_status": "Paid", "latest_contribution_period": "2026-07"},
        },
        "digilocker": {
            "status": "compliant", "last_updated": "2026-08-30T10:00:00Z", "confidence": 0.95,
            "raw_fields": {"consent_status": "Granted", "identity_document_verified": True, "authorized_signatory_verified": True, "credential_issued_at": "2026-08-30T09:58:00Z"},
        },
        "blacklist": {
            "status": "compliant", "last_updated": "2026-09-01T06:00:00Z", "confidence": 0.93,
            "raw_fields": {"registry_match": False, "debarment_status": "Not listed", "registry_search_reference": "BLR-20260901-004"},
        },
    },
}


def verify_profile(bidder_id: str, source: str) -> dict:
    """Return an isolated, normalized source result for a known bidder."""
    profile = PROFILES.get(bidder_id.upper())
    if profile is None:
        return {
            "source": source,
            "status": "not_found",
            "last_updated": "2026-09-01T06:00:00Z",
            "raw_fields": {"bidder_id": bidder_id, "registry_match": False},
            "confidence": 0.0,
        }

    result = deepcopy(profile[source])
    return {"source": source, **result}
