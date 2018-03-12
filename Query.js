//5.3.1 Course Search by Keyword
db.course.aggregate(
	[
		{$match:{"cid":"COMP4332"}},
		{
			$lookup:{
				from:"timeslot",
				localField:"cid",
				foreignField :"cid",
				as:"course_timeslot"
				}
		},
		{$unwind:"$course_timeslot"},
		{$match:{"course_timeslot.tid": "2018-02-15 00:30"}},
		{
			$lookup:{
				from:"section",
				localField:"course_timeslot.sid",
				foreignField:"sid",
				as:"course_timeslot_section"
			}
		},
		{$unwind:"$course_timeslot_section"},
		{$project:{cid:1,name:1,no_of_credit:1 ,_id:0,course_timeslot_section:1  }}

	]
)

//5.3.2 Course Search by Waiting List Size
db.course.aggregate(
	[
		{
			$lookup:{
				from:"timeslot",
				localField:"cid",
				foreignField :"cid",
				as:"course_timeslot"
				}
		},
		{$unwind:"$course_timeslot"},
		{$match:{"course_timeslot.tid":{$gte:"2018-02-10 00:30"}}},
		{$match:{"course_timeslot.tid":{$lte:"2018-02-16 00:30"}}},
		{
			$lookup:{
				from:"section",
				localField:"course_timeslot.sid",
				foreignField:"sid",
				as:"course_timeslot_section"
			}
		},
		{$unwind:"$course_timeslot_section"},
		{$project:{cid:1,name:1,no_of_credit:1 ,_id:0,course_timeslot_section:1  }}

	]
)


