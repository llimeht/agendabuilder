# AgendaBuilder making organising meetings easier

AgendaBuilder aims to make it easier to organise the details of effective
meetings, using a traditional layout for an agenda and meeting pack with
information.

## Usage

Step 1: create a meeting.yaml file that describes the meeting.

Step 2: build the agenda document.
```
agenda-builder.py agenda meeting.yaml
```

Step 3: edit the ageda document and create a final PDF of the agenda.

Step 4: combine the agenda and all the appendices into a meeting pack.
```
agenda-builder.py pack meeting.yaml
```

Step 5: distribute the meeting pack to your attendees so that they arrive at
the meeting properly briefed.

