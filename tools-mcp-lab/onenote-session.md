# OneNote server capabilities

**Session ID:** ses_e0b80b748ffe16C4ytzh4VKCOJ
**Created:** 11/19/2026, 10:49:04 AM
**Updated:** 11/19/2026, 10:52:40 AM

---

## User

what tools does the onenote server give you?

---

## Assistant (Build · Big Pickle · 11.3s)

_Thinking:_

The user is asking about what tools the onenote server gives me. Let me look at the available tools from the onenote MCP server that are listed in my system prompt. Let me enumerate them from the function definitions.

Let me look at the function definitions provided:
- onenote_download-bytes
- onenote_download-bytes-to-file
- onenote_get-onenote-page-content
- onenote_list-accounts
- onenote_list-all-onenote-sections
- onenote_list-onenote-notebook-sections
- onenote_list-onenote-notebooks
- onenote_list-onenote-pages
- onenote_list-onenote-section-groups
- onenote_list-onenote-section-pages
- onenote_verify-login

Note the user asks about "the onenote server" - what tools it gives me. I should answer concisely. Let me list the onenote-prefixed tools.

Actually, the question is a direct question about my capabilities / tools. This is informational. I should answer concisely. I don't need to fetch docs since this is about the local MCP server tools which are already enumerated in my context.

Let me count and list them.

The onenote-prefixed tools are:
1. onenote_download-bytes
2. onenote_download-bytes-to-file
3. onenote_get-onenote-page-content
4. onenote_list-accounts
5. onenote_list-all-onenote-sections
6. onenote_list-onenote-notebook-sections
7. onenote_list-onenote-notebooks
8. onenote_list-onenote-pages
9. onenote_list-onenote-section-groups
10. onenote_list-onenote-section-pages
11. onenote_verify-login

That's 11 tools. I should present them concisely with brief descriptions. The user asked for detail essentially - "what tools does the onenote server give you?" So a list is appropriate. But I should keep it reasonably concise. Given the instruction to be concise with fewer than 4 lines unless asked for detail - the user is asking for a list of tools, which is detail-oriented. I'll provide a compact grouped list.

Note: these are actually Microsoft Graph tools exposed via the onenote MCP server. Let me group them.

I'll give a concise grouped answer.

The OneNote MCP server exposes these tools:

- **Auth/account**: `verify-login`, `list-accounts`
- **Notebooks**: `list-onenote-notebooks`, `list-onenote-notebook-sections`
- **Sections**: `list-all-onenote-sections`, `list-onenote-section-groups`, `list-onenote-section-pages`
- **Pages**: `list-onenote-pages`, `get-onenote-page-content`
- **Binary content**: `download-bytes`, `download-bytes-to-file`

It's read-only; Graph write operations are disabled.

---

## User

List the notebooks available in my OneNote account.

---

## Assistant (Build · Big Pickle · 5.4s)

_Thinking:_

The user wants me to list the notebooks in their OneNote account. I should use the onenote_list-onenote-notebooks tool. Let me call it.

**Tool: onenote_list-onenote-notebooks**

**Input:**
```json
{
  "top": 50,
  "select": "id,displayName,isDefault,isShared,createdTime,lastModifiedTime"
}
```

**Error:**
```
{"error":"Microsoft Graph API error: 400  - {\"error\":{\"code\":\"BadRequest\",\"message\":\"Parsing OData Select and Expand failed: Could not find a property named 'createdTime' on type 'microsoft.graph.notebook'.\",\"innerError\":{\"date\":\"2026-11-19T15:52:13\",\"request-id\":\"8ef57d49-016a-4f9c-b47a-621d5a75fc78\",\"client-request-id\":\"8ef57d49-016a-4f9c-b47a-621d5a75fc78\"}}}"}
```

---

## Assistant (Build · Big Pickle · 4.6s)

_Thinking:_

The notebook object doesn't have createdTime. Let me use valid fields: id, displayName, isDefault, isShared, lastModifiedTime, sectionsUrl, sectionGroupsUrl, self, userRole, isReadOnly.

**Tool: onenote_list-onenote-notebooks**

**Input:**
```json
{
  "top": 50,
  "select": "id,displayName,isDefault,isShared,lastModifiedTime"
}
```

**Error:**
```
{"error":"Microsoft Graph API error: 400  - {\"error\":{\"code\":\"BadRequest\",\"message\":\"Parsing OData Select and Expand failed: Could not find a property named 'lastModifiedTime' on type 'microsoft.graph.notebook'.\",\"innerError\":{\"date\":\"2026-11-19T15:52:17\",\"request-id\":\"8dbbd45e-15af-4b2e-b460-aebcc4769bb3\",\"client-request-id\":\"8dbbd45e-15af-4b2e-b460-aebcc4769bb3\"}}}"}
```

---

## Assistant (Build · Big Pickle · 8.3s)

_Thinking:_

Notebook has no lastModifiedTime either. Let me just use id, displayName, isDefault, isShared.

**Tool: onenote_list-onenote-notebooks**

**Input:**
```json
{
  "top": 50,
  "select": "id,displayName,isDefault,isShared"
}
```

**Output:**
```
{"value":[{"id":"0-657466BD3832CC4D!s1dfb7a76ffa84a4b867707251dd079ac","displayName":"CS357","isDefault":false,"isShared":false},{"id":"0-657466BD3832CC4D!s405d8cd040c249efb4f99ff3e453980e","displayName":"To do list","isDefault":false,"isShared":false}]}
```

---

## Assistant (Build · Big Pickle · 3.2s)

Your OneNote notebooks:

1. **CS357**
2. **To do list**

Neither is shared or the default notebook.

---

## User

what is 17 times 23

---

## Assistant (Build · Big Pickle · 3.6s)

_Thinking:_

17 × 23 = 391.

391

---

