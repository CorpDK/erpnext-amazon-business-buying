# erpnext-amazon-business-buying

Frappe v16 app **`erpnext_amazon_business_buying`** for Amazon Business **Punch-in** checkout approval: purchase requests, approver workflow, and punch-in audit log.

## Dependencies

- ERPNext v16
- **[erpnext-amazon-business](https://github.com/CorpDK/erpnext-amazon-business)** (`erpnext_amazon_business`) — storefront master, OAuth, and relay pairing (buying settings do **not** duplicate pairing fields)

## P0 scope (this repo)

- DocTypes: Buying Settings (+ punch-in storefront secrets), Buying Company Config (+ cost-center approvers and buyer map), Purchase Request (+ items), Punch-in Log
- Workflow **Amazon Business Purchase Request Approval** (roles **Amazon Business Buyer** / **Amazon Business Approver**, created on install/migrate)
- **Amazon Business Buyer**: own purchase requests only (`buyer_user` list filter; identity defaulted from session; no delete)
- **Buyer User / Buyer Email** on saved requests: only **System Manager** may reassign (approvers and buyers cannot)
- Desk workspace **Amazon Business Buying** (no separate apps-screen entry)
- CI: Ruff + unit tests (bench migrate job skeleton)

Out of scope here: relay Punch-in HTTP, POOM fetch workers, StatusUpdateRequest jobs (B1+).

## Install

```bash
bench get-app https://github.com/CorpDK/erpnext-amazon-business-buying
bench --site <site> install-app erpnext_amazon_business_buying
```

Install **erpnext_amazon_business** first, then assign **Amazon Business Buyer** and **Amazon Business Approver** to users who will create or approve purchase requests.

## License

GPL-3.0-or-later — see [LICENSE](LICENSE).
