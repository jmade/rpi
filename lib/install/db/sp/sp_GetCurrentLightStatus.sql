-- call sp_GetLastBackgroundPID();
-- SELECT `pid` FROM `background` ORDER BY id DESC LIMIT 1;


drop procedure if exists sp_GetCurrentLightStatus;

delimiter //

create procedure sp_GetCurrentLightStatus()

begin

insert into background(
	pid,
	name
)
values(
	pPid,
	pName
);

end;
//

delimiter ;