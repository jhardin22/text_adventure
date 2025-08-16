# Blue Room Story

## Entry (start)
*Act: introduction*

A man sits at a desk in the room, writing in a book. He looks up as you enter and smiles. Hope and excitement inexplicably swell again.

"Wow, I've been here for ages. It's good to see you. I've been alone for a long time. Would you like to sit with me?"

**Choices:**
- [SIT] → sit_branch
- [TALK] → talk_branch  
- [LEAVE] → leave_branch

## Sitting Together (sit_branch)
*Act: bonding, Parent: SIT*

You sit down and start talking to the man. He tells you about his life and how he has been cursed to stay in the room. As the two of you talk the feeling of hope and excitement ebbs and flows. Something inside of you is drawn to the man and the room.

"Will you marry me?"

The question comes out of nowhere. You're not sure how to respond at first, but the longer you sit with the question the more certain you become.

**Choices:**
- [Say yes] → proposal_yes (REWARD: blue_token, FLAG: blue_room_complete)
- [Say no] → proposal_no (FLAG: blue_room_complete)

## Proposal Accepted (proposal_yes)
*Act: resolution, Terminal: true*

You accept with a smile. The room seems to glow, and the moment settles warmly into your heart. The man gives you a small blue token as a keepsake of this moment.

**END**