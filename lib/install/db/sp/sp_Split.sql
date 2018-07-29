/*
Created by: JSD
Date: 20090427
Desc: This routine splits a comma seperated string into a tmp table.
*/


drop procedure if exists sp_Split;

delimiter //

create procedure sp_Split(
	in pIdList varchar(8000)
	, out prc int
)

begin
main: begin

declare vL int;  # vL is the Left hand position
declare vR int;  # vR is the Right hand position
declare vId bigint;

create temporary table tmpSplit (
  Id varchar(20)
) engine = memory;

if length(pIdList) < 1
then
	select 'Error in Split list.  Code SPLIT012.' as DBErrorMsg;
	set prc = -1;
	leave main;
end if;

set vL = 1;

loop1: loop

	set vR = locate(',', pIdList, vL+1);
	if vR = 0 
	then # we're on the last one
		if vL = 1  # it's also the first one
		then
			insert into tmpSplit (Id) values (pIdList);
		else
			insert into tmpSplit (Id) values (substring(pIdList, vL+1));
		end if;

		leave loop1;
	end if;

	if vL = 1
	then
		insert into tmpSplit (Id) values (substring(pIdList, vL, vR-vL));
	else
		insert into tmpSplit (Id) values (substring(pIdList, vL+1, (vR-vL)-1));
	end if;

	set vL = vR;

end loop loop1;


set prc = 0;

end main;
end;
//

delimiter ;

