---
name: ready-items-user-story
description: Review GitHub Project Ready items and add missing User Story and Acceptance Criteria to their issues based on each work item's title.
---

# Ready items: User Story and Acceptance Criteria

Use this skill when asked to review a GitHub Project's `Ready` column and complete issue descriptions.

## Workflow

1. Identify the target project number and owner from the request.
2. List the project's items with:

   ```powershell
   gh project item-list <project-number> --owner <owner> --query "status:Ready" --format json --limit 200
   ```

3. Process only items whose content is an issue. For each issue, read the current description:

   ```powershell
   gh issue view <issue-number> --repo <owner>/<repo> --json number,title,body,url
   ```

4. Treat a section as present only when the body contains a heading for that section:
   - User Story: `## User Story`
   - Acceptance Criteria: `## Acceptance Criteria`

5. If both sections are present, do not modify the issue.
6. If either section is missing, write content from the work item's title:
   - User Story must use the format `身為...，我希望...，以便...。`
   - Acceptance Criteria must be a testable Markdown bullet list covering valid input, validation/error handling, expected behavior, and visible output where applicable.
7. Preserve all existing issue content. Add only missing sections, separated from existing content by a blank line. Do not overwrite an existing User Story or Acceptance Criteria section.
8. Update the issue with:

   ```powershell
   gh issue edit <issue-number> --repo <owner>/<repo> --body <updated-body>
   ```

9. Re-read every modified issue and verify that the required headings and generated content are present.

## Writing guidance

- Infer the actor, goal, and benefit directly from the title; do not invent unrelated scope.
- Make criteria observable and independently verifiable.
- Prefer 3–6 criteria per feature.
- Include deterministic behavior when calculations or classifications are involved.
- Use the language of the issue title unless the requester specifies another language.
- Do not change project status, labels, assignees, milestones, or issue titles.

## Safety checks

- Never process items outside the `Ready` status.
- Never modify an issue when both required sections already exist.
- If an issue is closed, report it and do not reopen it.
- If the title or current body is ambiguous, preserve existing text and state what could not be inferred instead of fabricating requirements.
