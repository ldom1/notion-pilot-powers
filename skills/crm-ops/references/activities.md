# Activities

Append-only event log. Model: `ActivityInput`. Never “upsert” an activity — always CREATE a new row.

## Type enum

`📞 Call` | `📧 Email` | `💼 LinkedIn` | `🎤 Demo` | `🤝 Meeting` | `📄 Proposal` | `🎪 Conference` | `✅ Task` | `📋 Other`

## Outcome enum

`✅ Positive` | `➡️ Follow-up Needed` | `❌ Negative` | `🔇 No Response`

## Properties

| Field | Notion | Notes |
|-------|--------|-------|
| title | `Name` | in the user's language, specific (not just “Email”) |
| type | `Type` | required |
| date | `Date` | ISO date of the event; defaults to today |
| duration_min | `Duration (min)` | minutes; optional |
| outcome | `Outcome` | |
| deal | `Deal` | relation → Lead |
| person | `Person` | relation → People |
| company | `Company` | relation → Companies |
| next_step | `Next Step` | in the user's language |
| next_step_date | `Next Step Date` | |
| notes | `Notes` | source language OK |
| done | `Done` | checkbox; tasks only |

## From email threads

Create one activity per meaningful event (send, reply, meeting). Link Deal + Person + Company when known. Planned future meetings: still CREATE with the planned date and Outcome `➡️ Follow-up Needed`.

## Tasks

A to-do ("send the proposal by Friday") is an Activity with Type `✅ Task`, `Next Step Date` = due date, `Done` unchecked, linked to the Deal. When the user says it is done, UPDATE that row: check `Done`. This is the one activity you update. If the database has no `✅ Task` option or no `Done`, set the Lead `Next Step` and date instead.
