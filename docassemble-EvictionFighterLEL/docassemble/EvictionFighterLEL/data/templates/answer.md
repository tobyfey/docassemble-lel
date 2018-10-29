---
"FirstFooterLeft": |-
  First of [TOTALPAGES] pages
  [END]
"HeaderLeft": |-
  Page [PAGENUM] of [TOTALPAGES]
  [END]
...

[BOLDCENTER] IN THE ${ courtNameAC } [NEWLINE]
${ countyAC }, OHIO

[BEGIN_CAPTION]

${ plaintiff }
  
  
Plaintiff,[NEWLINE]
  
  
[TAB]v.[NEWLINE]
  
  
${ defendant }
  
  
Defendant.
  
  
[VERTICAL_LINE]

CASE NO. ${ casenumber }[NEWLINE]
  
  
  
JUDGE: ${ judge }[NEWLINE]
  
  
  
${ title }[NEWLINE]

[END_CAPTION]

[BOLDCENTER] NOTICE CONCERNING PRO SE STATUS

Defendant is low-income and unable to afford an attorney, and has not been able to get any attorney to represent them.  Defendant is not licensed to practice law, and is not knowledgeable in the practice of law for purposes of presenting a case in court.

[BOLDCENTER] ANSWER

Unless Defendant specifically admits the allegations made by Plaintiff in the Complaint, Defendant denies the allegations in the Complaint.

% for answer in sortedanswers:
1. ${ answer.conclusion }
% endfor

[BOLDCENTER] AFFIRMATIVE DEFENSES

Defendant incorporates all prior paragraphs in the following defenses.

% for legalobject in sorteddefenses:

[BOLDCENTER] AFFIRMATIVE DEFENSE ${ legalobject.indexnumber } [BR]
${ legalobject.title }

1. ${ legalobject.law }
% for fact in legalobject.facts:
1. ${ fact.factstatement }
% for evidence in fact.evidence:
% if not fact.evidence.typeofevidencedefault == "NA":
${ evidence.evidencestatement }
% endif
% endfor
% endfor
1. ${ legalobject.conclusion }
% endfor


[BOLDCENTER] DEMAND FOR JUDGMENT

For the above, reasons, Defendant requests that:[NEWLINE]
1. Plaintiff's Complaint be dismissed, at Plaintiff's cost,[NEWLINE]
2. and any other appropriate remedies.[NEWLINE]

[INDENTBY 3in][BLANKFILL]                    
${ defendant }, Pro Se Defendant  
${ defendantstreetaddress }  
${ defendantcitystatezip }  
% if defendantphonenumber:
${ defendantphonenumber }[NEWLINE]
% endif

[BOLDCENTER] PROOF OF SERVICE

On the date of [BLANKFILL]            (month/day/year), a copy of this ${ title } was mailed by U.S. regular mail, postage prepaid, to ${ lawyer }, ${ lawyerstreetaddress }, ${ lawyercitystatezip }.

[INDENTBY 3in][BLANK] [NEWLINE]

[INDENTBY 3in]${ defendant }, Pro Se Defendant


This document was created using Eviction Fighter, an online tool for self-represented litigants.
