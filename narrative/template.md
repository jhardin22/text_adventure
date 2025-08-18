# Story Room Template

<!--
- Description: first quoted line in the first node becomes JSON "description".
- Choices: use '- [Text] -> target_id' (ASCII '->' recommended).
- Rewards: place '(REWARD: item_id)' inside the TERMINAL node’s prose (nodes with no Choices).
- Flags: per-choice flags are not emitted by the converter or allowed by the schema.
         Use the room-level completion_flag in the generated JSON.
- Node IDs: letters/digits/underscores only (## Title (node_id)).
-->

## Entry (start)

"This is the room-wide description shown on entry. It will populate the JSON 'description' field."

You arrive in a place that feels like a memory. Light, air, and a sense of something important.

Choices:

- [Sit with the man] -> sit_branch
- [Talk for a while] -> talk_leaf
- [Leave the memory] -> leave_leaf

## Sitting Together (sit_branch)

You sit together. The conversation turns to what comes next. What do you do?

Choices:

- [Share vows] -> vows_leaf
- [Ask about the past] -> past_leaf

## Vows Memory (vows_leaf)

You remember a promise spoken softly. The moment crystallizes around a single, shining detail. (REWARD: wedding_band)

## Past Memory (past_leaf)

You sift through the past, finding comfort in the stories that brought you here.

## A Quiet Talk (talk_leaf)

You share simple words and the quiet between them. The feeling lingers, warm and bright.

## Leaving (leave_leaf)

You let the memory fade and step back, ready to return to where you began.
