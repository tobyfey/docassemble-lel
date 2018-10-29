% if len(affidavitlist) > 0:
[PAGEBREAK]


[BOLDCENTER]AFFIDAVIT



% for aff in affidavitlist:
${ aff.number }. ${ aff.testimony }

% endfor

[INDENTBY 3in][BLANKFILL][BR]
[INDENTBY 3in]AFFIANT
% endif
