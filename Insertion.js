db.course.insert(
	{	
		cid:"COMP4332",
		name:"Big Data Management",
		no_of_credit: 3,
		description: "This course will expose students to new and practical issues of real world mining and managing big data. Data mining and management is to effectively support storage, retrieval, and extracting implicit, previously unknown, and potentially useful knowledge from data. This course will place emphasis on two parts. The first part is big data issues such as mining and managing on distributed data, sampling on big data and using some cloud computing techniques on big data. The second part is applications of the techniques learnt on areas such as business intelligence, science and engineering, which aims to uncover facts and patterns in large volumes of data for decision support. This course builds on basic knowledge gained in the introductory data-mining course, and explores how to more effectively mine and manage large volumes of real-world data and to tap into large quantities of data. Working on real world data sets, students will experience all steps of a data-mining and management project, beginning with problem definition and data selection, and continuing through data management, data exploration, data transformation, sampling, portioning, modelling, and assessment.",
		remarks: "Instructor Consent Required",
		pre_requisite_list: [
			 {code: "COMP4211" },
			 {code: "COMP4331"},
			 {code: "ISOM 3360" },
			],
		exclude_list: [
			{code: "COMP4621"},
			{code: "COMP3333"}
			]

	}
)

db.timeslot.insert(
	{
		tid: "2018-02-15 00:30",
		cid: "COMP4332",
		sid: 1918

	}
)

db.section.insert(
	{
		sid:1918,
		cid:"COMP4332",
		section: "L1",
		datetime:[
			{time:"Wed 01:30PM - 02:50PM"},
			{time:"Fri 01:30PM - 02:50PM"}
		],
		room: "G010",
		instructor: "WONG, Raymond Chi Wing",
		quota: 65,
		enrol: 0,
		avail: 65
	}

)


