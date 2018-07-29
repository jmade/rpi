-- call sp_InsBackground('0000','test_process');

drop procedure if exists sp_InsBackground;

delimiter //

create procedure sp_InsBackground(
	in pPid VARCHAR(10),
	in pName VARCHAR(36)
)

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