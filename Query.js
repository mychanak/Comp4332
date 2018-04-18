
//find the lastest time slot
//used by 5.3.1 and 5.3.2
db.course.aggregate([
	{$unwind: "$listOfSections"},
	
	//find the lastest time slot
	{$group: {_id:"$code",maxDate:{$max: "$listOfSections.timeSlot"}}},
	{$out: "R1"}
])


//5.3.1 Course Search by Keyword
//Keyword: "Risk Mining"
//Sorting in ascending order of "Sections" within a single course in Python



db.course.aggregate([
    { $match: { $or: [{ ctitle: /.*Risk.*/ }, { description: /.*Risk.*/ }, { "listOfSections.remarks": /.*Risk.*/ }, { ctitle: /.*Mining.*/ }, 
	{ description: /.*Mining.*/ }, { "listOfSections.remarks": /.*Mining.*/ }] } },
	{$lookup:{
		localField: "code",
		from: "R1",
		foreignField: "_id",
		as: "R3"
	}},
	{$unwind: "$R3"},
	{$unwind: "$listOfSections"},
    {$project: { _id: 0, code: 1, ctitle: 1, credit: 1, "listOfSections.section": 1, "listOfSections.dateTime": 1, "listOfSections.quota": 1, "listOfSections.enrol": 1, "listOfSections.avail": 1, "listOfSections.wait": 1 ,compareResult: {$eq: ["$listOfSections.timeSlot", "$R3.maxDate"]} } },
    {$match: {compareResult: true}},
    {$group: {_id: { "code": "$code","ctitle": "$ctitle" ,"credit":"$credit"}, "listOfSections":{"$addToSet": "$listOfSections"}}},
    {$unwind:"$listOfSections"},
    {$sort:{"listOfSections.section":1}},
    { $group: {_id: { "code": "$_id.code","ctitle": "$_id.ctitle" ,"credit":"$_id.credit"}, "listOfSections":{"$push": "$listOfSections"}}},
    {$project:{code:"$_id.code",ctitle:"$_id.ctitle",credit:"$_id.credit", listOfSections:"$listOfSections",_id:0}},
    { $sort: { code: 1} }
])

//5.3.2 Course Search by Waiting list size
//f: 0.05, start_ts: 2018-01-26T14:00:00Z, end_ts: 2018-02-01T11:30:00Z

db.course.aggregate([
	//find the list of sections between start_ts and end_ts
	{$match: {
        $and: [{ "listOfSections.timeSlot": { $gte: new Date("2018-01-26T14:00:00Z") } }, 
        	{ "listOfSections.timeSlot": { $lte: new Date("2018-02-01T11:30:00Z") } }
        ]}},
	{$unwind: "$listOfSections"},
	
	//find the lastest time slot
	{$group: {_id:"$code",maxDate:{$max: "$listOfSections.timeSlot"}}},
	{$out: "R2"}
])

db.course.aggregate([
	//join the table with R1
	{$lookup:{
		localField: "code",
		from: "R1",
		foreignField: "_id",
		as: "R3"
	}},
	{$unwind: "$R3"},
	{$project:{_id: 0, code:1, ctitle:1, credit:1, "listOfSections.section": 1, "listOfSections.dateTime": 1, "listOfSections.quota": 1, "listOfSections.enrol": 1, "listOfSections.avail": 1, "listOfSections.wait": 1, "listOfSections.timeSlot": 1, "R3.maxDate":1}},
	{$unwind: "$listOfSections"},
	
	//find the sections with time slot = maxDate
	{$project:{_id: 0, code:1, ctitle:1, credit:1, "listOfSections.section": 1, "listOfSections.dateTime": 1, "listOfSections.quota": 1, "listOfSections.enrol": 1, "listOfSections.avail": 1, "listOfSections.wait": 1, "listOfSections.timeSlot": 1, "R3.maxDate":1, compareResult: {$eq: ["$listOfSections.timeSlot", "$R3.maxDate"]} }},
	{$match: {compareResult: true}},
	
	//output the information
	{$project:{_id: 0, code:1, ctitle:1, credit:1, "listOfSections.section": 1, "listOfSections.dateTime": 1, "listOfSections.quota": 1, "listOfSections.enrol": 1, "listOfSections.avail": 1, "listOfSections.wait": 1, match_ts:"$R3.maxDate" }},
	{ $group: {_id: { "code": "$code","ctitle": "$ctitle" ,"credit":"$credit" ,"match_ts":"$match_ts"}, "listOfSections":{"$addToSet": "$listOfSections"}}},
	{$unwind:"$listOfSections"},
    {$sort:{"listOfSections.section":1}},
    { $group: {_id: { "code": "$_id.code","ctitle": "$_id.ctitle" ,"credit":"$_id.credit", "match_ts":"$_id.match_ts"}, "listOfSections":{"$push": "$listOfSections"}}},
	{$project:{code:"$_id.code",ctitle:"$_id.ctitle",credit:"$_id.credit", match_ts:"$_id.match_ts" ,listOfSections:"$listOfSections",_id:0}},
	{ $sort: { "_id.code": 1 } }
])
		
db.R1.drop()
