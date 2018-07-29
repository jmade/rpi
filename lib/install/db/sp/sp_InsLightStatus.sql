-- call sp_InsLightStatus('Y','test_1234');

drop procedure if exists sp_InsLightStatus;

delimiter //

create procedure sp_InsLightStatus(
	in pActive VARCHAR(1),
	in pName VARCHAR(10)
)

begin

insert into lightStatus(
	active,
	process
)
values(
	pActive,
	pName
);

end;
//

delimiter ;