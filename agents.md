# Splunk Environment Documentation for AI Assistants

Structured reference for generating efficient SPL queries. Discovered via Splunk MCP tools.

---

### Indexes

| Index | Purpose | Notes |
|-------|---------|--------|
| **main** | Primary application and infrastructure data | ~500K events; HTTP, Kubernetes container logs, auth, syslog. Use for app analytics, security, and correlation. |
| **_internal** | Splunk server operations | splunkd, splunkd_access, scheduler, mongod, node sidecar logs. Use for troubleshooting and license/usage. |
| **_introspection** | Splunk resource and telemetry metrics | splunk_resource_usage, kvstore, search_telemetry, http_event_collector_metrics. Use for performance and HEC metrics. |
| **_audit** | User and admin audit trail | Audit events for compliance and access review. |
| **_configtracker** | Configuration change tracking | Track config changes over time. |
| **summary** | Summary/indexed analytics | Default summary index; currently empty. Use for `collect`/scheduled search rollups. |
| **_telemetry** | Product telemetry | Minimal event count. |
| **_dsappevent**, **_dsclient**, **_dsphonehome** | Deployment/phone-home (empty) | Reserved for deployment server. |
| **_thefishbucket** | Fishbucket (empty) | Internal indexing state. |
| **history** | Search history (empty) | Optional search history store. |
| **splunklogger** | Logger (disabled) | Disabled index. |

**Query tips:** Prefer `index=main` for app/security; `index=_internal` for Splunk health; `index=_introspection` for resource/search metrics. Restrict time range for large indexes.

---

### Sourcetypes

**Index: main** (application and Kubernetes)

- **httpevent** — HTTP/API events (high volume); use for status, method, URI, response time.
- **auth_log** — Auth/session events (e.g. pam_unix, cron sessions); correlate by user, host.
- **syslog** — Syslog; host, facility, message.
- **kube:container:*** — Kubernetes container stdout per service, e.g.:
  - `kube:container:frontend`, `kube:container:cart`, `kube:container:payment`, `kube:container:ad`, `kube:container:image-provider`, `kube:container:recommendation`, `kube:container:fraud-detection`, `kube:container:kafka`, `kube:container:postgresql`, `kube:container:mssql`, `kube:container:sqlserver`, `kube:container:email`, `kube:container:quote`, `kube:container:shop-dc-shim`, `kube:container:astronomy-loadgen`, `kube:container:valkey-cart`, others.
- **kube:events** — Kubernetes events (pod/node).
- **kube:object:events** — Kubernetes object events.
- **kube:object:pods** — Pod metadata/state.

**Index: _internal** (Splunk platform)

- **splunkd**, **splunkd_access**, **splunkd_ui_access**, **splunk_web_access**, **splunk_web_service** — Splunk daemon and UI access.
- **splunk_search_messages**, **splunkd_conf**, **splunkd_stderr** — Search and config.
- **node:sidecar:*** — CMP/orchestrator, identity, postgres, ipc_broker, etc.
- **node:supervisor** — Supervisor logs.
- **mongod**, **postgres** — Internal DB logs.
- **scheduler**, **mcp_server** — Scheduler and MCP server.
- **splunk_first_install**, **splunk_version**, **splunk_o11y_app** — Install/version/app.

**Index: _introspection**

- **splunk_resource_usage** — Resource usage metrics.
- **kvstore** — KV store operations.
- **search_telemetry** — Search telemetry.
- **http_event_collector_metrics** — HEC metrics.
- **splunk_disk_objects**, **splunk_telemetry** — Disk and telemetry.

**Query tips:** Filter by `sourcetype=` or `sourcetype=httpevent` for HTTP; `sourcetype=kube:*` for all Kubernetes data; `sourcetype=starts_with("kube:container:")` for container logs only.

---

### Lookups

**CSV / file-based (enrichment and examples)**

- **geo_attr_countries** — country, region_wb, region_un, subregion, continent, iso2, iso3.
- **geo_attr_us_states** — state_name, state_fips, state_code.
- **geo_countries**, **geo_us_states** — Geo (KMZ) for mapping.
- **dnslookup** — clienthost, clientip (DNS enrichment).
- **pura_mark_public_as_private** — app_folder_name (visibility).
- **campus_example**, **examples**, **firewall_example**, **outages_example**, **security_example_data**, **geomaps_data** — Example/demo data.

**KV Store (app state and UI)**

- **era_***, **jra_***, **pra_*** — Email receivers, page visits, dismiss app/file, export report, schedule scan, send email, notification switches.
- **pra_user_records** — host_name, user_name, user_role, action, request_timestamp, description, stack_id.
- **ura_clear_cache_global**, **ura_clear_cache_local** — Cache clear state (last_clear_time, hostname).

**Query tips:** Use `lookup geo_attr_countries country OUTPUT region_un continent` or `| lookup dnslookup clientip OUTPUT clienthost`. Prefer exact lookup key names from fields_list above.

---

### Data Models

| Model | Purpose |
|-------|---------|
| **internal_audit_logs** | Audit log data model (app=search). |
| **internal_server** | Internal server/data model (app=search). |

Acceleration is disabled for both. Use `| from datamodel ...` or Pivot/datamodel-aware searches when building reports from these models.

---

### Summary Indexes

- **summary** — Default summary index; present and enabled; **0 events** in current environment. No saved searches in the sampled set write to a summary index.
- For analytics, use scheduled searches with `action.summary_index = 1` and target index `summary` (or a custom summary index) to populate; then query that index for dashboards and rollups.

---

### Key Fields

**Universal (all events)**  
`_time`, `index`, `host`, `source`, `sourcetype`, `linecount`, `_raw`.

**Correlation and identity**  
- **host** — Hostname (e.g. k3d node, ip-172-31-80-136).  
- **user** — User identity (auth_log, access logs).  
- **src_ip**, **dest_ip** — When present (firewall, proxy, HTTP).  
- **clientip** — Client IP (use with dnslookup for clienthost).

**HTTP / httpevent**  
- **status**, **method**, **uri** (or **url**) — When extracted by props.

**Kubernetes**  
- **pod**, **container**, **namespace**, **container_id** — When present in kube:container:* or kube:object:*.

**Auth / security**  
- **user**, **action**, **result** — In auth_log and similar.

**Time**  
- **\_time** — Always use for time range; pair with `earliest_time`/`latest_time` in API.

**Query tips:** Start with `index=main host=*` or `index=main sourcetype=httpevent` and add `| stats count by host, sourcetype` or `by user, status` as needed. Use `host`, `sourcetype`, and `_time` for efficient filters.

---

*Generated for Splunk MCP; update after major index/sourcetype or data model changes.*
