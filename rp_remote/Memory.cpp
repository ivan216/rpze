#include "stdafx.h"
#include "Memory.h"

#define __until(expr) do {} while (!(expr))

Memory::Memory(DWORD pid)
{
	auto fileName = std::wstring{ SHARED_MEMORY_NAME_AFFIX }.append(std::to_wstring(pid));
	hMemory = OpenFileMappingW(FILE_MAP_ALL_ACCESS, FALSE, fileName.c_str());
	if (hMemory == NULL)
	{
		std::cerr << "寻找共享内存失败: " << GetLastError() << std::endl;
		throw std::exception("find shared memory failed");
	}
	pBuf = MapViewOfFile(hMemory, FILE_MAP_ALL_ACCESS, 0, 0, 1024);
	if (pBuf == NULL)
	{
		std::cerr << "创建文件视图失败: " << GetLastError() << std::endl;
		throw std::exception("create shared memory failed");
	}
	else
	{
		std::cout << "寻找共享内存成功" << std::endl;
	}

	pCurrentPhaseCode = &getPhaseCode();
	pCurrentRunState = &getRunState();
}

std::optional<volatile void*> Memory::_readMemory(BYTE size,const std::initializer_list<int32_t>& offsets)
{
	getMemoryNum() = size;
	int idx = 0;
	for (auto it : offsets)
	{
		getOffsets()[idx] = it;
		idx++;
	}
	getOffsets()[idx] = OFFSET_END;
	getCurrentPhaseCode() = PhaseCode::READ_MEMORY;
	__until(getCurrentPhaseCode() == PhaseCode::WAIT);//等待执行完成
	if (getExecuteResult() == ExecuteResult::SUCCESS) return getReadResult();
	if (getExecuteResult() == ExecuteResult::FAIL) return {};
	throw std::exception("unexpected behavior");
}

bool Memory::_writeMemory(const void* pVal, BYTE size, const std::initializer_list<int32_t>& offsets)
{
	getMemoryNum() = size;
	memcpy(getWrittenVal(), pVal, size);
	int idx = 0;
	for (auto it : offsets)
	{
		getOffsets()[idx] = it;
		idx++;
	}
	getOffsets()[idx] = OFFSET_END;

	getCurrentPhaseCode() = PhaseCode::WRITE_MEMORY;
	__until(getCurrentPhaseCode() == PhaseCode::WAIT);  //等待执行完成
	if (getExecuteResult() == ExecuteResult::SUCCESS) return true;
	if (getExecuteResult() == ExecuteResult::FAIL) return false;
	throw std::exception("unexpected behavior");
}

bool Memory::startJumpFrame()
{
	if (isJumpingFrame) return false;
	isJumpingFrame = true;
	pCurrentPhaseCode = &getJumpingPhaseCode();
	pCurrentRunState = &getJumpingRunState();
	getJumpingPhaseCode() = PhaseCode::WAIT;
	getPhaseCode() = PhaseCode::JUMP_FRAME;
	return true;
}

bool Memory::endJumpFrame()
{
	if (!isJumpingFrame) return false;
	isJumpingFrame = false;
	pCurrentPhaseCode = &getPhaseCode();
	pCurrentRunState = &getRunState();
	getPhaseCode() = PhaseCode::WAIT;
	getJumpingPhaseCode() = PhaseCode::CONTINUE;
	return true;
}

#undef __until