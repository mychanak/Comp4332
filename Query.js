//5.3.1 Course Search by Keyword
//Keyword: "Risk Mining"
//Sorting in ascending order of "Sections" within a single course in Python

db.course.aggregate([
    { $match: { $or: [{ ctitle: /.*Risk.*/ }, { description: /.*Risk.*/ }, { "listOfSections.remarks": /.*Risk.*/ }, { ctitle: /.*Mining.*/ }, 
{ description: /.*Mining.*/ }, { "listOfSections.remarks": /.*Mining.*/ }] } },

    { $project: { _id: 0, code: 1, ctitle: 1, credit: 1, "listOfSections.section": 1, "listOfSections.dateTime": 1, "listOfSections.quota": 1, "listOfSections.enrol": 1, "listOfSections.avail": 1, "listOfSections.wait": 1 } },

    { $sort: { code: 1 } }
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
	{$out: "R1"}
])

db.course.aggregate([
	//join the table with R1
	{$lookup:{
		localField: "code",
		from: "R1",
		foreignField: "_id",
		as: "R2"
	}},
	{$unwind: "$R2"},
	{$project:{_id: 0, code:1, ctitle:1, credit:1, "listOfSections.section": 1, "listOfSections.dateTime": 1, "listOfSections.quota": 1, "listOfSections.enrol": 1, "listOfSections.avail": 1, "listOfSections.wait": 1, "listOfSections.timeSlot": 1, "R2.maxDate":1}},
	{$unwind: "$listOfSections"},
	
	//find the sections with time slot = maxDate
	{$project:{_id: 0, code:1, ctitle:1, credit:1, "listOfSections.section": 1, "listOfSections.dateTime": 1, "listOfSections.quota": 1, "listOfSections.enrol": 1, "listOfSections.avail": 1, "listOfSections.wait": 1, "listOfSections.timeSlot": 1, "R2.maxDate":1, compareResult: {$eq: ["$listOfSections.timeSlot", "$R2.maxDate"]} }},
	{$match: {compareResult: true}},
	
	//output the information
	{$project:{_id: 0, code:1, ctitle:1, credit:1, "listOfSections.section": 1, "listOfSections.dateTime": 1, "listOfSections.quota": 1, "listOfSections.enrol": 1, "listOfSections.avail": 1, "listOfSections.wait": 1, match_ts:"$R2.maxDate" }},
	{ $group: {_id: { "code": "$code","ctitle": "$ctitle" ,"credit":"$credit" ,"match_ts":"$match_ts"}, "listOfSections":{"$addToSet": "$listOfSections"}}},
	{ $sort: { "_id.code": 1 } }
])
		
db.R1.drop()
