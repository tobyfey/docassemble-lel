USE ONLY ONE PLAYGROUND WINDOW, ACROSS ALL DEVICES, AT A TIME!!!  OTHERWISE LOSE YOUR WORK!

# Table of contents
1. [Initial Blocks](#initialblocks)
	1. [Imports and Metadata](#importsandmetadata)
	1. [Variables](#variables)
	1. [Objects](#objects)
		1. [Auto Gather](#autogather)
1. [User Questions](#userquestions)
	1. [Preliminary Information](#preliminaryinformation)
		1. [Establishing Jurisdiction](#establishingjurisdiction)
		1. [Selecting Legal Action](#selectinglegalaction)
	1. [Legal Objects](#legalobjects)
		1. [Creating Children Legal Objects](#creatingchildrenlegalobjects)
			1. [Legal Object AirTable Function](#legalobjectairtablefunction)
		1. [Asking Which Legal Objects Are Relevant](#askinglegalobjectrelevant)
			1. [Converting dict to attributes](#convertingdicttoattributes)
		1. [Legal Object ismet](#legalobjectismet)
			1. [LegalObjectList ismet](#legalobjectlistismet)
		1. [LegalObject class](#legalobjectclass)
	1. [Fact Objects](#factobjects)
		1. [Creating Children Fact Objects](#creatingchildrenfactobjects)
			1. [Fact Object AirTable Function](#factobjectairtablefunction)
		1. [Fact Object Questions](#factobjectquestions)
		1. [Fact Object ismet](#factobjectismet)
	1. [Evidence](#evidence)
		1. [Asking if there is more evidence](#askingevidence)
		1. [Evidence Class](#evidenceclass)
1. [Documents](#documents)
	1. [Answer](#answer)
		1. [Caption](#caption)
		1. [Answer Section](#answersection)
		1. [Affirmative Defenses](#affirmativedefenses)
		1. [Remedies](#remedies)
		1. [Signature](#signature)
	1. [Other Documents](#otherdocuments)
		1. [Exhibit List](#exhibitlist)
		1. [Affidavit](#affidavit)
		1. [Findings of Fact](#findingsoffact)
			1. [Conclusions of Law](#conclusionsoflaw)
	1. [Instructions](#instructions)
		1. [Nested methods](#nestedmethods)
	

To determine if the parent legal object is met, the interview should go through all the relevant children legal objects to determine if they are met (but it may only go through the relevant children legal objects that are necessary - for example, if preconditions isn't me because of lack of corporate registration, will it determine if lack of representation is met?).

Once it has been determined whether the parent legal object was met, then it should sort the answer legal objects (possibly based on user input about the complaint - default is preconditions, grounds, notice) and then sort the met children legal objects for the affirmative defenses (based on 'strength',.

A code block then assigns exhibit numbers and affidavit numbers by going through the sorted list and fact children.  (All the fact children or just the ones that the defendant needs to dispute?  For now, I will stick with all, but this should be tested.) The fact children and the relevant number are added to the appropriate list (exhibit, affidavit, finding of facts, conclusion of law).

What about remedies and tools?  In this same code block, I guess potential remedies and tools should also be added to the list

# Initial Blocks<a name="initialblocks"></a>
## Imports and Metadata<a name="importsandmetadata"></a>

```yaml
metadata:
  title: Eviction Fighter
  short title: evictionfighter TESTING ONLY
---
modules:
  - docassemble.base.util
  - .airtable
  - .auth
  - .params
  - .legalobject
---
imports:
  - requests
  - yaml
  - json
  - datetime
---
```
Libraries are also imported in legalobject.py

```python
from docassemble.base.core import DAObject, DAList
from docassemble.base.util import get_config, Thing
from docassemble.base.functions import word
from .airtable import Airtable
```

## Variables<a name="variables"></a>

Two static variables used for accessing the AirTable are set in legalobject.py.  The airtable api key is set in the config file.  (When I tried to make this variable with underscores instead of spaces, it didn't work.)

```python
base_key = 'appVibGdpOZq6nKPT'
api_key=get_config('airtable api key')
```

## Objects<a name="objects"></a>

The foundation of the Legal Elements Library is the use of Legal Objects.  The Eviction Fighter asks questions to determine what Legal Elements/Objects are relevant, then provides information stored as structured data in the relevant Legal Objects.

The sets and lists are for collecting the legalobjects that are "met" and have information in attributes that should be used.  During the interview, the objects are collected in sets to avoid duplicate objects.  Before the documents are generated, the sets are sorted into lists.  

I got rid of sets because sets are immutable.  Instead, there will be a function that will add an object to a list, if there is no unique object in the list already.  If there is, we will add object.parent to the existing object (in order to have a list of the reasons a remedy or tool is selected)

The Legal Objects are listed in legalobject.yml.  We can also set attributes of Legal Objects to special classes of Legal Objects by using generic objects.

```yaml
objects:
  - legalobjects: LegalObjectList.using(object_type=LegalObject,auto_gather=False)
  - answerlist: DAList
  - defenseslist: DAList
  - remedieslist: DAList
  - exhibitlist: DAList
  - affidavitlist: DAList
  - findingsoffactlist: DAList
  - conclusionsoflawlist: DAList
  - toolslist: DAList
  - evidencelist: EvidenceList
---
generic object: LegalObject
objects:
  - x.children: LegalObjectList.using(object_type=LegalObject,auto_gather=False)

```
The classes of Legal Objects are also defined in legalobject.py
**TODO**



### Auto Gather<a name="autogather"></a>

Objects that are in the class DAList have an automatic gathering system, where the interview will ask if there are any members of the list or if there is another.  To avoid this feature, objects have to have auto.gather set to False, and gathered has to be set to True.  You can also set True to gathered in a code block after something that needs to happen (like legalobjects.gathered).

```yaml
mandatory: True
code: |
  legalobjects.auto_gather = False
  answerlist.auto_gather = False
  defenseslist.auto_gather = False
  remedieslist.auto_gather = False
  exhibitlist.auto_gather = False
  affidavitlist.auto_gather = False
  findingsoffactlist.auto_gather = False
  conclusionsoflawlist.auto_gather = False
  toolslist.auto_gather = False
  remedieslist.gathered = True
  exhibitlist.gathered = True
  affidavitlist.gathered = True
  findingsoffactlist.gathered = True
  conclusionsoflawlist.gathered = True
  toolslist.gathered = True
  answerlist.gathered = True
  defenseslist.gathered = True
  evidencelist.auto_gather = True
  evidencelist.there_are_any = False
---
```


### Establishing Jurisdiction<a name="establishingjurisdiction"></a>

First, we must answer the questions that will determine what law applies for a specific case, or, in other words, what set of legal objects are relevant.  These questions will determine the state and local jurisdiction and the type of housing, which will determine what rules and laws apply to a particular user.

This first version is made for Ohio law.  When we expand, we will add a question to determine location.

Currently, we only have a simple list of housing types.  The same list makes the options for the 'typeofhousing' field in the AirTable.

This section can also be reworked so [typeofhousing] is set with a series of easy to use questions.

```yaml
---
question: Type of Housing
fields:
  - Do you know the type of housing you live in?: typeofhousingknown
    datatype: yesnowide
  - Pick a type of housing: typeofhousing
    show if: typeofhousingknown
    choices:
      - A1 Private Housing
      - A2 Mobile Home Lot Rental
      - A3 Section 8 Certificates and Vouchers
      - A4 HUD Subsidized Projects
      - A5 Moderate Rehabilitation Projects
      - A6 Project-Based Certificate Projects
      - A7 Rural Housing Service Projects
      - A8 Public Housing
  - What best describes your type of housing?: housingtypedescription
    hide if: typeofhousingknown
    choices:
      - I do not get any type of housing subsidy
      - I live in a mobile home park
      - I have a voucher
      - I live in public housing owned by a housing authority
      - I live in subsidized housing
      - Other
---
code: |
  if housingtypedescription == "I do not get any type of housing subsidy":
    typeofhousing = "A1 Private Housing"
  if housingtypedescription == "I live in a mobile home park":
    typeofhousing = "A2 Mobile Home Lot Rental"
  if housingtypedescription == "I have a voucher":
    typeofhousing = "A3 Section 8 Certificates and Vouchers"
  if housingtypedescription == "I live in public housing owned by a housing authority":
    typeofhousing = "A8 Public Housing"
---
code: |
  if housingtypedescription == "I live in subsidized housing.":
    housingtype = "A4 HUD Subsidized Projects"
---
```


### Selecting Legal Action<a name="selectinglegalaction"></a>
Once we have the jurisdiction set, the legal action must be set.  A parent legal object (a legal object that does not have a parent itself) is a legal action - a type of action filed in court.  Currently, we only have eviction, but typical legal actions related to rental housing also include a landlord claim for damages (which will be added next, because a landlord claim for damages is often included with an eviction action), a tenant claim for damages (which might include a security deposit claim or damages due to discrimination under fair housing laws), and a tenant action to get the court to order repairs to be made.

This is a question where the content is actually in the yaml question.  If the user selects Eviction, then a_id is set to the record id for the row for the Eviction legal object.  This string is generated by AirTable.  I need to figure out a better way to determine what record ids are.  Right now I either look at the [AirTable API](https://airtable.com/appA5wMpmdl4Vo8Kb/api/docs#curl/table:elements:list) or at the variable output at the end of an interview.

When we have more actions, we may want to generate from AirTable a dictionary with label:id for each parent legal object.

We may also want to add help, hint, or default.  Currently we can do that in the yaml question.


```yaml
question: |
  What is the legal action?
fields:
  - Type: a_id
    input type: radio
    choices:
      - Eviction: recB0J8H7GkpRuQ80
---
code: |
  legalobjects.append(object_from_a_id(a_id))
  legalobjects.gathered = True
---
```

<img width="600" src="img/parentlegalobject.jpg">


## Legal Objects<a name="legalobjects"></a>

### Creating Children Legal Objects<a name="creatingchildrenlegalobjects"></a>

The filtering for type of housing occurs when the children legal objects are appended to the LegalObjectList.

Couldn't the filter happen when the parent object is gathered?  

```yaml
generic object: LegalObject
code: |
  for atid in x.childrenlist:
    tempobject = object_from_a_id(atid)
    if tempobject.active:
      if typeofhousing in tempobject.typeofhousing:
        x.children.append(tempobject,set_instance_name=True)
  x.children.gathered = True
---
```


#### Legal Object AirTable Function<a name="legalobjectairtablefunction"></a>

The function object_from_a_id sets the attributes for a legal object based on AirTable fields.  The function takes the id number for a row in AirTable.  (It can be tricky to figure out what the id is - I should look into if there is an easier way.)

Notice that some of the fields set attributes of funcobject.facts, instead of setting attributes of funcobject itself.  funcobject.facts is also initialized as a FactObjectList if a certain attribute (follabel) is found.

Is there a way to do this automatically based on field names?  Would we have to do the factobjectlist attributes seperately?

FIELDS TO ADD


FIELDS TO REMOVE
- .name?
- .note?

```python
def object_from_a_id(a_id):
	funcobject = LegalObject()
	table_name = 'Elements'
	api_response = Airtable(base_key, table_name, api_key)
	el = api_response.get(a_id)
	if 'field' in el['fields']:
		funcobject.field = el['fields']['field']
	if 'label' in el['fields']:
		funcobject.name = el['fields']['label']
		funcobject.label = el['fields']['label']
	if 'typeofhousing' in el['fields']:
		funcobject.typeofhousing = el['fields']['typeofhousing']
	funcobject.id = el['id']
	if 'datatype' in el['fields']:
		funcobject.datatype = el['fields']['datatype']
	else:
		funcobject.datatype = 'yesno'
	if 'Active' in el['fields']:
		funcobject.active = el['fields']['Active']
	else:
		funcobject.active = False
	if 'pleadingsection' in el['fields']:
		funcobject.pleadingsection = el['fields']['pleadingsection']
	else:
		funcobject.pleadingsection = 'none'
	if 'help' in el['fields']:
		funcobject.help = el['fields']['help']
	if 'image' in el['fields']:
		funcobject.image = el['fields']['image']
	if 'default' in el['fields']:
		funcobject.default = el['fields']['default']
	if 'note' in el['fields']:
		funcobject.note = el['fields']['note']
	if 'children' in el['fields']:
		funcobject.childrenlist = el['fields']['children']
	if 'facts' in el['fields']:
		funcobject.factslist = el['fields']['facts']
	if 'parent' in el['fields']:
		funcobject.parent = el['fields']['parent']
	if 'question' in el['fields']:
		funcobject.question = el['fields']['question']
	if 'explanation' in el['fields']:
		funcobject.explanation = el['fields']['explanation']
	if 'explanationbottom' in el['fields']:
		funcobject.explanationbottom = el['fields']['explanationbottom']
	if 'explanationifmet' in el['fields']:
		funcobject.explanationifmet = el['fields']['explanationifmet']
	if 'explanationifnotmet' in el['fields']:
		funcobject.explanationifnotmet = el['fields']['explanationifnotmet']
	if 'follabel' in el['fields']:
		funcobject.initializeAttribute('facts', FactObjectList)
		funcobject.facts.label = el['fields']['follabel']
	if 'folhtml' in el['fields']:
	   funcobject.facts.html = el['fields']['folhtml']
	if 'folexplanation' in el['fields']:
		funcobject.facts.explanation = el['fields']['folexplanation']
	if 'folquestion' in el['fields']:
		funcobject.facts.question = el['fields']['folquestion']
	if 'comparisontype' in el['fields']:
		funcobject.facts.comparisontype = el['fields']['comparisontype']
	if 'title' in el['fields']:
		funcobject.title = el['fields']['title']
	if 'law' in el['fields']:
		funcobject.law = el['fields']['law']
	if 'conclusion' in el['fields']:
		funcobject.conclusion = el['fields']['conclusion']
	return funcobject
```
<img width="600" src="img/airtableelements1.jpg">

### Asking Which Legal Objects Are Relevant<a name="askinglegalobjectrelevant"></a>

This block produces a question screen for users to determine if the children LegalObjects are relevant.

<img width="600" src="img/legalobjectchildrenquestion.jpg">

```yaml
generic object: LegalObject
question:  ${ x.label }
subquestion: |
  % if hasattr(x,'explanation'):
  ${ x.explanation }
  % endif
  
  % if hasattr(x,'question'):
  ${ x.question }
  % endif
  
fields:
  - no label: x.childrendict
    datatype: checkboxes
    code: x.questioncode()
---
```
The method x.questioncode is defined in legalobject.py for the class LegalObject.  The method pulls information from attributes of the LegalObject children for the question.

```python
class LegalObject(DAObject):

	def questioncode(self):
		questioncode = []
		for child in self.children:
			adict = {}
			adict[child.id] = child.label
			if hasattr(child,'help'):
				adict[u'help'] = child.help
			if hasattr(child,'default'):
				adict[u'default'] = child.default
			questioncode.append(adict)
		return questioncode
```

Here is an example of asking if the children of a child legal object are relevant.

<img width="600" src="img/legalobjectchildrenquestion2.jpg">

#### Converting dict to attributes<a name="convertingdicttoattributes"></a>

True and False can be switched in order to allow the following type of interaction- the user picks a child legal object to investigate by unclicking the checkbox, rather than clicking it.

```yaml
generic object: LegalObject
sets: x.children[0].isrelevant
code: |
  for chi in x.children:
    if x.childrendict[chi.id]:
      chi.isrelevant = True
    else:
      chi.isrelevant = False
---
```

### Legal Object ismet<a name="legalobjectismet"></a>

This block sets .ismet for an object based on both its LegalObject children and FactObject children.  Since the final screen needs to know if a relevant legal object is met, this block makes docassemble find.

This section will need to add the legalobject to the answer or affirmative defense section, depending on an attribute for the legalobject.  It will also be added to the conclusions of law section.  (Add in a motion to dismiss section next?)


```yaml
---
generic object: LegalObject
code: |
  if factsgathered:
    if not hasattr(x, 'factslist') or x.facts.ismet:
      if not hasattr(x, 'childrenlist') or x.children.ismet:
        x.ismet = True
      else:
        x.ismet = False
        if 'Answer' in x.pleadingsection:
          answerlist.append(x)
        elif 'AffirmativeDefense' in x.pleadingsection:
          defenseslist.append(x)
        conclusionsoflawlist.append(x)
    else:
      if not hasattr(x, 'childrenlist'):
        x.ismet = False
        if 'Answer' in x.pleadingsection:
          answerlist.append(x)
        elif 'AffirmativeDefense' in x.pleadingsection:
          defenseslist.append(x)
        conclusionsoflawlist.append(x)
      else:
        if x.children.ismet:
          x.ismet = True
        else:
          x.ismet = False
          if 'Answer' in x.pleadingsection:
            answerlist.append(x)
          elif 'AffirmativeDefense' in x.pleadingsection:
            defenseslist.append(x)
          conclusionsoflawlist.append(x)

---
---
```


#### LegalObjectList ismet<a name="legalobjectlistismet"></a>

The children LegalObjects are in a LegalObjectList that is an attribute of the parent LegalObject.  LegalObjectLists such as x.children have their own attributes, including ismet.  Whether a LegalObject is met depends on whether x.children.ismet

```yaml
---
generic object: LegalObjectList
code: |
  counter = 0
  for legalobject in x:
    if legalobject.isrelevant and not legalobject.ismet:
      if legalobject.pleadingsection == "AffirmativeDefense" and not legalobject in defenseslist:
        defenseslist.append(x)
      if legalobject.pleadingsection == "Answer" and not legalobject in answerlist:
        answerlist.append(x)
    else:
      counter += 1
  if counter == len(x):
    x.ismet = True
  else:
    x.ismet = False
	
---
```

### LegalObject class<a name="legalobjectclass"></a>

```python
class LegalObject(DAObject):
	def ___init___(self, *pargs, **kwargs):
		self.initializeAttribute('children', LegalObjectList.using(object_type=LegalObject))
		self.initializeAttribute('facts', FactObjectList.using(object_type=FactObject))
		return super(LegalObject, self).init(*pargs, **kwargs)

```

## Fact Objects<a name="factobjects"></a>

What is the problem with the fact.field label?  Why can't I do that through an alias?  I made a change in fact_from_aid that may work

```python
class FactObject(Thing):
	def ___init___(self, *pargs, **kwargs):
 		self.initializeAttribute('children', LegalObjectList.using(object_type=LegalObject))
		return super(FactObject, self).init(*pargs, **kwargs)

```

### Creating Children Fact Objects<a name="creatingchildrenfactobjects"></a>

If a LegalObject has a facts attribute, after the LegalObject is added in the above block, then FactObjects are added to the LegalObject's FactObjectList with the following block.

```yaml
generic object: LegalObject
sets: 
  - x.facts
code: |
  if hasattr(x,'factslist'):
    x.facts.there_are_any = True
    for fid in x.factslist:
      x.facts.append(fact_from_a_id(fid),set_instance_name=True)
    x.facts.there_is_another = False
  else:
    x.facts.there_are_any = False
---
```

#### Fact Object AirTable Function<a name="factobjectairtablefunction"></a>
FactObjects are populated from a different AirTable than Elements.  This also sets information for the EvidenceList, which is stored in each

I replaced funcobject.field = el['fields']['field'] with funcobject.field = funcobject.instanceName
Maybe that will allow me to not have to write in instance names in the field

Fact Objects do not have children themselves, but are part of a legal object that can have both facts and children.

<img width="600" src="img/airtablefacts.jpg">

```python
def fact_from_a_id(a_id):
	funcobject = FactObject()
	table_name = 'Facts'
	api_response = Airtable(base_key, table_name, api_key)
	el = api_response.get(a_id)
	funcobject.field = el['fields']['fieldold']
	funcobject.label = el['fields']['label']
	funcobject.id = el['id']
	funcobject.datatype = el['fields']['datatype']
	if 'help' in el['fields']:
		funcobject.help = el['fields']['help']
	if 'hint' in el['fields']:
		funcobject.hint = el['fields']['hint']
	if 'image' in el['fields']:
		funcobject.image = el['fields']['image']
	if 'default' in el['fields']:
		funcobject.default = el['fields']['default']
	if 'note' in el['fields']:
		funcobject.note = el['fields']['note']
	if 'parent' in el['fields']:
		funcobject.parent = el['fields']['parent'][0]
	if 'question' in el['fields']:
		funcobject.question = el['fields']['question']
	if 'explanation' in el['fields']:
		funcobject.explanation = el['fields']['explanation']
	if 'explanationbottom' in el['fields']:
		funcobject.explanationbottom = el['fields']['explanationbottom']
	if 'explanationifmet' in el['fields']:
		funcobject.explanationifmet = el['fields']['explanationifmet']
	if 'explanationifnotmet' in el['fields']:
		funcobject.explanationifnotmet = el['fields']['explanationifnotmet']
	if 'prefact' in el['fields']:
		funcobject.prefact = el['fields']['prefact']
	else:
		funcobject.prefact = ""
	if 'postfact' in el['fields']:
		funcobject.postfact = el['fields']['postfact']
	else:
		funcobject.postfact = ""
	if 'typeofevidence' in el['fields'] and not el['fields']['typeofevidence'] == 'NA':
		funcobject.initializeAttribute('evidence', EvidenceList.using(object_type=Evidence))
		funcobject.evidence.typeofevidence = el['fields']['typeofevidence']
		if 'evlabel' in el['fields']:
			funcobject.evidence.label = el['fields']['evlabel']
		else:
			funcobject.evidence.label = ""
		if 'evexplanation' in el['fields']:
			funcobject.evidence.explanation = el['fields']['evexplanation']
		else:
			funcobject.evidence.explanation = ""
		if 'evquestion' in el['fields']:
			funcobject.evidence.question = el['fields']['evquestion']
		else:
			funcobject.evidence.question = ""
		if 'typeofevidencedefault' in el['fields']:
			funcobject.evidence.typeofevidencedefault = el['fields']['typeofevidencedefault']
		if 'evhint' in el['fields']:
			funcobject.evidence.default = el['fields']['evhint']
	return funcobject
```
### Fact Object Questions<a name="factobjectquestions"></a>

This question will ask the fact questions needed to determine if a legal object is met.

Fact questions can have different kinds of datatypes as inputs, unlike LegalObject children questions which are yes and no questions.

<img width="600" src="img/factobjectquestion.jpg">

```yaml
generic object: FactObjectList
sets: x[0]
question:  ${ x.label }
subquestion: |
  ${ x.explanation }
  
  ${ x.question }

  % if hasattr(x,'html'):
  ${ x.html }
  % endif
  
  
fields:
  code: x.questioncode()
---
```
The questioncode is a method of the class FactObjectList.  However, the data for the FactObjectList is part of the Elements AirTable, not the Facts AirTable, because a legal object has a single FactObjectList as an attribute (which will have FactObjects if it is a defense or the final branch of the children tree.

```python
class FactObjectList(DAList):

	def questioncode(self):
		questioncode = []
		for factt in self:
			adict = {}
			adict['field'] = factt.field
			adict['label'] = factt.label
			adict['datatype'] = factt.datatype
			if hasattr(factt,'help'):
				adict[u'help'] = factt.help
			if hasattr(factt,'hint'):
				adict[u'hint'] = factt.hint
			if hasattr(factt,'image'):
				adict[u'image'] = factt.image
			if hasattr(factt,'default'):
				adict[u'default'] = factt.default
			if hasattr(factt,'note'):
				adict[u'note'] = factt.note
			questioncode.append(adict)
		return questioncode
		
```
### Fact Object ismet<a name="factobjectismet"></a>

This section has the different ways a Fact Object List can be met, because of an interaction between the fact objects defined here.

This list can be added to any time a different type of interaction is needed.  By keeping this section flexible and human readable, we can scale this project as needed to different kinds of information.

Fact Objects and yesnowide vs noyeswide - a Fact Object that is a yes or no question should usually be asked in a way where the "Yes" answer means the tenant wins.  So "Did you pay rent on time?" would be a yesnowide, because a yes answer would be a good defense.  "Did you pay your rent late?"  would be a noyeswide, because a no answer would be a good defense.

1. Equals - if two of the fact objects are the same
1. 2AllTrue - if both fact objects are true
1. 1AllTrue - if the only fact object is true
1. 3AllTrue
1. 4AnyTrue
1. CompareDate
1. CompareDateAmount

ADD LINK TO AIRTABLE FOR COMPARISONTYPE

**This section will have to add facts to sets for exhibit lists, affidavit and findings of fact.**  Should I make a method for this?

```yaml
---
generic object: FactObjectList
sets:
  - x.ismet
code: |
  if x.comparisontype == "Equals":
		if x[0].value == x[1].value:
			x.ismet = True
		else:
      if x[1].evidence.typeofevidencedefault == "NA" or x[1].evidence[0].typeofevidence:
			  x.ismet = False
  if x.comparisontype == "2AllTrue":
    if x[0].value and x[1].value:
      if x[0].evidence.typeofevidencedefault == "NA" or x[0].evidence[0].typeofevidence:
        if x[1].evidence.typeofevidencedefault == "NA" or x[1].evidence[0].typeofevidence:
          x.ismet = False
    else:
      x.ismet = True
  if x.comparisontype == "1AllTrue":
    if x[0].value:
      if x[0].evidence.typeofevidencedefault == "NA" or x[0].evidence[0].typeofevidence:
        x.ismet = False
    else:
      x.ismet = True
  if x.comparisontype == "3AllTrue":
    if x[0].value and x[1].value and x[2].value:
      if x[0].evidence.typeofevidencedefault == "NA" or x[0].evidence[0].typeofevidence:
        if x[1].evidence.typeofevidencedefault == "NA" or x[1].evidence[0].typeofevidence:
          if x[2].evidence.typeofevidencedefault == "NA" or x[2].evidence[0].typeofevidence:
            x.ismet = False
    else:
      x.ismet = True
  if x.comparisontype == "2AnyTrue":
    Any2TrueCounter = 0
    if not x[0].value and not x[1].value:
      x.ismet = True
    else:
      for ctfact in x:
        if ctfact.value == True:
          if ctfact.evidence.typeofevidencedefault == "NA" or ctfact.evidence[0].typeofevidence:
            Any2TrueCounter += 1
      if Any2TrueCounter > 0:
        x.ismet = False
  if x.comparisontype == "3AnyTrue":
    Any3TrueCounter = 0
    if not x[0].value and not x[1].value and not x[2]:
      x.ismet = True
    else:
      for ctfact in x:
        if ctfact.value == True:
          if ctfact.evidence.typeofevidencedefault == "NA" or ctfact.evidence[0].typeofevidence:
            Any3TrueCounter += 1
      if Any3TrueCounter > 0:
        x.ismet = False
  if x.comparisontype == "4AnyTrue":
    Any4TrueCounter = 0
    if not x[0].value and not x[1].value and not x[2] and not x[3]:
      x.ismet = True
    else:
      for ctfact in x:
        if ctfact.value == True:
          if ctfact.evidence.typeofevidencedefault == "NA" or ctfact.evidence[0].typeofevidence:
            Any4TrueCounter += 1
      if Any4TrueCounter > 0:
        x.ismet = False
  if x.comparisontype == "CompareDate":
    tempdate0 = as_datetime(x[0].value)
    tempdate1 = as_datetime(x[1].value)
    tempdate2 = as_datetime(x[2].value)
    if tempdate0.plus(days=3) >= tempdate1 or tempdate1 < tempdate2:
      if x[0].evidence.typeofevidencedefault == "NA" or x[0].evidence[0].typeofevidence:
        if x[1].evidence.typeofevidencedefault == "NA" or x[1].evidence[0].typeofevidence:
          if x[2].evidence.typeofevidencedefault == "NA" or x[2].evidence[0].typeofevidence:
            x.ismet = False
    else:
      x.ismet = True
  if x.comparisontype == "CompareDate2":
    tempdate0 = as_datetime(x[0].value)
    tempdate1 = as_datetime(x[1].value)
    if tempdate0.plus(years=2) > tempdate1:
      if x[0].evidence.typeofevidencedefault == "NA" or x[0].evidence[0].typeofevidence:
        if x[1].evidence.typeofevidencedefault == "NA" or x[1].evidence[0].typeofevidence:
            x.ismet = True
    else:
      x.ismet = False
  if x.comparisontype == "CompareDate3":
    tempdate0 = as_datetime(x[0].value)
    tempdate1 = as_datetime(x[1].value)
    if tempdate0 >= tempdate1:
      if x[0].evidence.typeofevidencedefault == "NA" or x[0].evidence[0].typeofevidence:
        if x[1].evidence.typeofevidencedefault == "NA" or x[1].evidence[0].typeofevidence:
            x.ismet = True
    else:
      x.ismet = False
  if x.comparisontype == "CompareDate4":
    tempdate0 = as_datetime(x[0].value)
    tempdate1 = as_datetime(x[1].value)
    if tempdate0.plus(weeks=1) >= tempdate1:
      x.ismet = True
    else:
      if x[0].evidence.typeofevidencedefault == "NA" or x[0].evidence[0].typeofevidence:
        if x[1].evidence.typeofevidencedefault == "NA" or x[1].evidence[0].typeofevidence:
          x.ismet = False
  if x.comparisontype == "CompareDateAmount":
    if as_datetime(x[0].value) >= as_datetime(x[2].value):
      if x[1].value <= x[3].value:
        if x[0].evidence.typeofevidencedefault == "NA" or x[0].evidence[0].typeofevidence:
          if x[1].evidence.typeofevidencedefault == "NA" or x[1].evidence[0].typeofevidence:
            if x[2].evidence.typeofevidencedefault == "NA" or x[2].evidence[0].typeofevidence:
              if x[3].evidence.typeofevidencedefault == "NA" or x[3].evidence[0].typeofevidence:
                x.ismet = False
      else:
        x.ismet = True
    else:
      x.ismet = True
    if x.comparisontype == "PercentageComparison":
      if x[0].value/x[1].value > .2:
        if x[0].evidence.typeofevidencedefault == "NA" or x[0].evidence[0].typeofevidence:
          if x[1].evidence.typeofevidencedefault == "NA" or x[1].evidence[0].typeofevidence:
            x.ismet = False
      else:
        x.ismet = True
---
---
```
### fact.value

The .value attributes in the comparison code are created by assigning the value of x.field (which is the variable name) to x.value.

```
---
generic object: FactObject
code: x.value = value(x.field)
---
```
### Pre-gathering all facts
To avoid problems with the back button used after questions where the facts are set using code, this section pre-defines all of the fact variables at the beginning of the interview.

```
---
code: |
  base_key = 'appVibGdpOZq6nKPT'
  table_name = 'Facts'
  api_response = Airtable(base_key, table_name, api_key='key2jDr134l25QZ9P')
  factsdict = api_response.get_all()
  for fact in factsdict:
    if 'Active' in fact['fields']:
      if fact['fields']['datatype'] == "yesnowide":
        define(fact['fields']['fieldold'], True)
      elif fact['fields']['datatype'] == "noyeswide":
        define(fact['fields']['fieldold'], False)
      else:
        define(fact['fields']['fieldold'], fact['fields']['default'])
  factsgathered = True
---
```

## Evidence<a name="evidence"></a>
### Determining whether evidence is relevant
``` yaml
---
generic object: FactObject
code: |
  if hasattr(x,'evidence') and not x.evidence.typeofevidencedefault == "NA" and x.value:
    x.evidence.there_are_any = True
  else:
    x.evidence.there_are_any = False
---
generic object: FactObject
code: |
  if hasattr(x.evidence[0],'typeofevidence') or not x.value:
    x.evidence.there_is_another = False
---

```
### Asking if there is more evidence<a name="askingevidence"></a>

- Needs to be asked only for facts that are relevant
- The evidencetype needs to determine what sets information is put in - testimony goes into an affidavit (a different one for each client)

Evidence is different than the LegalObject and Facts children - it isn't asking multiple questions for multiple children.  It is asking one question - How do you prove that fact? - and allowing multiple answers

Certain fields should be shown depending on type of evidence
- Documents: Title
- Plaintiff's Evidence: ParagraphOrExhibit, PoENumber
- Testimony: Statement
- WitnessTestimony: Statement, Name of Witness, Relation, Age

I should be able to ask if the evidence was evidence already submitted.

There will also be a number attribute, to keep track of the exhibit number or affidavit number.

```yaml
---
generic object: FactObject
question: How can you prove ${ x.evidence.label }?
subquestion: |
  ${ x.evidence.explanation }
  
  ${ x.evidence.question }

  % if hasattr(x,'evidence.html'):
  ${ x.evidence.html }
  % endif
fields:
 - Evidence already included: x.evidence[i]
   datatype: object
   choices: 
    - evidencelist
 - Type of evidence: x.evidence[i].typeofevidence
   input type: radio
   required: True
   choices:
     - Documents: documents
     - Photographs: documents
     - Plaintiff's evidence: plaintiffevidence
     - Witness testimony: witnesstestimony
     - Your testimony: testimony
     - Judicial notice: judicialnotice
   default: ${ x.evidence.typeofevidencedefault }
 - Title: x.evidence[i].title
   show if:
     variable: x.evidence[i].typeofevidence
     is: documents
 - Paragraph in complaint or Exhibit?: x.evidence[i].paragraphOrExhibit
   choices:
     - Paragraph
     - Exhibit
   show if:
     variable: x.evidence[i].typeofevidence
     is: plaintiffevidence
 - Number?: x.evidence[i].poenumber
   datatype: integer
   show if:
     variable: x.evidence[i].typeofevidence
     is: plaintiffevidence 
 - Describe: x.evidence[i].testimony
   datatype: area
   show if:
     variable: x.evidence[i].typeofevidence
     is: testimony 
 - What is the public source if information?: x.evidence[i].publicsource
   datatype: area
   default: ${ x.evidence.default }
   show if:
     variable: x.evidence[i].typeofevidence
     is: judicialnotice
---
```
### evidencelist

Maybe I should get a new name, but the evidencelist is intended to be a list of all evidence that the user submits, and allow them to reuse that evidence for another fact question.

```yaml
---
generic object: FactObject
sets: evidencelist[0]
code: |
  if hasattr(x.evidence[i], 'typeofevidence'):
    evidencelist.append(x.evidence[i])
  evidencelist.there_is_another = False


```
### Evidence Class<a name="evidenceclass"></a>

I should remove the initializeAttribute for children

The evexplanation method takes the information for each piece of evidence and makes an explanation for it and adds the Evidence object to AffidavitSet or ExhibitSet, for example "See Exhibit 2 - Receipt 10/17/2018"
x.exhibit = x.evexplanation()

```python
class EvidenceList(DAList):
		
	pass

class Evidence(DAObject):
  
	pass



```
# Documents<a name="documents"></a>
## Answer<a name="answer"></a>
### Sorting answers and defenses and assigning exhibit and affidavit numbers

This code block is intended to run after it has been determined if legalobjects[0].ismet (whether the eviction case has been met.  It organizes the answers and defenses, sorting the defenses by the .strength attribute.  It puts the answers and defenses into sortedanswers and sorteddefenses, which is referenced in the answer.

It also creates .evidencestatement attributes for evidence objects, which are used in the answer.
```yaml
---
code: |
  exhibitnumber = 1
  affidavitnumber = 1
---
code: |
  indexnumbercounter = 1
  sortedanswers = sorted(answerlist, key=lambda x:x.strength)
  sorteddefenses = sorted(defenseslist, key=lambda x:x.strength)
  for sd in sorteddefenses:
    sd.indexnumber = indexnumbercounter
    indexnumbercounter += 1
  totalanswers = sortedanswers + sorteddefenses
  for sa in totalanswers:
    sa.newattribute = "New"
    if hasattr(sa,'facts'):
      sa.newattributefact = "Facts"
      for fact in sa.facts:
        if hasattr(fact,'evidence'):
          sa.newattributeevidence = "evidence"
	        for ev in fact.evidence:
	          if hasattr(ev,'number'):
              sa.newattributeevidencenumber = "evidencenumber"
	            pass
	          else:
	            if ev.typeofevidence == 'documents':
	              ev.number = exhibitnumber
		            exhibitnumber += 1
		            ev.evidencestatement = "See Exhibit " 
		            ev.evidencestatement += str(ev.number)
		            ev.evidencestatement += ": "
		            ev.evidencestatement += str(ev.title)
                ev.evidencestatement += "."
                exhibitlist.append(ev)
	            elif ev.typeofevidence == "testimony":
	              ev.number = affidavitnumber
		            affidavitnumber += 1
		            ev.evidencestatement = "See Affidavit Paragraph " 
		            ev.evidencestatement += str(ev.number)
                ev.evidencestatement += "."
                affidavitlist.append(ev)
	            elif ev.typeofevidence == 'plaintiffevidence':
	              ev.evidencestatement = "See Plaintiff's "
		            if ev.paragraphOrExhibit == 'Paragraph':
		              ev.evidencestatement += " Paragraph "
		            else:
		              ev.evidencestatement += " Exhibit "
		            ev.evidencestatement += str(ev.poenumber)
                ev.evidencestatement += "."
              elif ev.typeofevidence == 'judicialnotice':
	              ev.evidencestatement = "The Court may take judicial notice of "
		            ev.evidencestatement += str(ev.publicsource)
                ev.evidencestatement += ", as it is a source whose accuracy cannot reasonably be questioned."
              else:
                pass
---
```
### Caption<a name="caption"></a>

<img width="600" src="img/captionquestions.jpg">

```yaml
question: Questions for the Caption
fields:
  - Name of Court in All Caps: courtNameAC
    default: Default Municipal Court
  - County in All Caps: countyAC
    default: BUTLER
  - Plaintiff: plaintiff
    default: Larry Landlord
  - Defendant: defendant
    default: Terry Tenant
  - Case Number: casenumber
    default: 18-CVG-99999
  - Judge: judge
    required: False
  - Title: title
    default: Answer
---
```

```markdown
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
```

### Answer Section<a name="answersection"></a>

```markdown
[BOLDCENTER] ANSWER

Unless Defendant specifically admits the allegations made by Plaintiff in the Complaint, Defendant denies the allegations in the Complaint.


% for answer in sortedanswers:
1. ${ answer.conclusion }
% endfor


```

### Affirmative Defenses<a name="affirmativedefenses"></a>

```markdown
% if len(metlegalobject) > 0):


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


```
#### .factstatement
The answer references an attribute of FactObjects called .factstatement.  That attribute is generated by this code block in the interview.
```yaml
generic object: FactObject
code: |
  x.factstatement = str(x.prefact)
  if x.datatype == 'text':
    x.factstatement += str(x.value)
  elif x.datatype == 'date':
    x.factstatement += as_datetime(x.value)
  elif x.datatype == 'currency':
    x.factstatement += str(x.value)
  x.factstatement += str(x.postfact)
---
```

### Remedies<a name="remedies"></a>

```markdown
[BOLDCENTER] DEMAND FOR JUDGMENT

For the above, reasons, Defendant requests that:[NEWLINE]
1. Plaintiff's Complaint be dismissed, at Plaintiff's cost,[NEWLINE]
2. and any other appropriate remedies.[NEWLINE]
```
### Signature<a name="signature"></a>
```markup
[INDENTBY 3in][BLANK]  
${ defendant }, Pro Se Defendant  
${ defendantstreetaddress }  
${ defendantcitystatezip }  
% if defendantphonenumber:
${ defendantphonenumber }[NEWLINE]
% endif

[BOLDCENTER] PROOF OF SERVICE

On the date of [BLANKFILL]  (month/day/year), a copy of this ${ title } was mailed by U.S. regular mail, postage prepaid, to ${ lawyer }, ${ lawyerstreetaddress }, ${ lawyercitystatezip }.

[INDENTBY 3in][BLANK] [NEWLINE]

[INDENTBY 3in]${ defendant }, Pro Se Defendant


This document was created using Eviction Fighter, an online tool for self-represented litigants.
```
These variables should be changed to attributes of DAObjects like [Person.](https://docassemble.org/docs/objects.html#tocAnchor-1-20-3)  

```yaml
question: Questions for the Signature
fields:
  - Defendant street address: defendantstreetaddress
    default: 123 Main St.
  - Defendant City State Zip: defendantcitystatezip
    default: Default, OH 43611
  - Defendant Phone Number: defendantphonenumber
    required: False
  - Lawyer: lawyer
    default: Larry Lawyer
  - Lawyer street address: lawyerstreetaddress 
    default: 321 High St.
  - Lawyer City State Zip: lawyercitystatezip
    default: Suburbs, OH 43666
---
```

## Other Documents<a name="otherdocuments"></a>

### Exhibit List<a name="exhibitlist"></a>

```markdown
% if exhibitlist:

% endif
```

### Affidavit<a name="affidavit"></a>

```markdown
% if affidavitlist:

% endif
```

### Findings of Fact<a name="findingsoffact"></a>

Users should get an option to add Findings of Fact and Conclusions of Law.

```markdown
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
```
#### Conclusions of Law<a name="conclusionsoflaw"></a>


## Instructions<a name="instructions"></a>

<img width="600" src="img/summary.jpg">

A docassemble interview is built from the mandatory summary block.  Because the block is mandatory, the program runs and finds out what variables need to be defined to complete the block.  Finding those variables is why all the other blocks are asked.

The summary block in Eviction Fighter should explain in plain english the eviction defenses that a user could argue in court.  This should include a list of the evidence needed.  If there are no defenses, the summary block should explain why the defenses the user investigated are not appropriate.





Currently, to test, the summary screen will say if sets are populated:

---
question: Summary
mandatory: True
subquestion: |

  % for lo in legalobjects:
  ${ lo.nestedexplain }
  
  % endfor

attachment:
  - name: Eviction Answer
    filename: EvictionAnswer
    content file:
      - answerDEV.md
      - affidavitDEV.md
      - exhibitDEV.md
---


The summary block will look for the exhibit and affidavit numbers, forcing this code block to run.  

This block will have to sort the legal objects, first by answer or defense (answer before by defense, and then by strength number ascending.)  Then it will have to go through the legal objects' facts, and then evidence, to put the evidence in order.  The code will assign the page number to the evidence object as an attribute.

### Nested methods<a name="nestedmethods"></a>

The nested methods are recursive methods, to build an explanation screen/hand-out 

I convert the method to an attribute - don't know if this is necessary.

```yaml
---
generic object: LegalObject
code: |
  x.nestedexplain = x.nested_explain()
---
```

```python
class LegalObject(DAObject):

	def nested_explain(self):
		fr = ""
		fr = str(self.label)
		fr += "\n"
		if self.ismet:
			fr += str(self.explanationifmet)
		else:
			fr += str(self.explanationifnotmet)
		fr += "\n"
		if hasattr(self, 'facts'):
			self.facts.nested_fact()
		if hasattr(self, 'children'):
			for child in self.children:
				if child.isrelevant:
					child.nested_explain()
		return fr
  
		
```

```python
class FactObjectList(DAList):

	def nested_fact(self):
		ff = ""
		for fact in self:
			ff = fact.factstatement
			ff += "\n"
			if hasattr(self,'evidence'):
				ff += "You can prove this with "
				for ev in fact.evidence:
					if ev.typeofevidence == 'Documents':
						ff += str(ev.title)
					elif ev.typeofevidence == 'Testimony':
						ff += "your testimony."
					elif ev.typeofevidence == 'plaintiffevidence':
						ff += "Plaintiff's "
						if ev.paragraphOrExhibit == 'paragraph':
							ff += " Paragraph "
						else:
							ff += " Exhibit "
						ff += str(ev.poenumber)
				ff += "\n"
		if hasattr(self, 'children'):
			for child in self.children:
				if child.isrelevant:
					ff += child.nested_explain()
		return ff

		
```


