#include "pch.h"
#include "SharedMemory.h"

SharedMemory* SharedMemory::instancePtr = nullptr;

SharedMemory::SharedMemory()
{
	auto hProc = GetCurrentProcess();
	sharedMemoryName = std::wstring(SHARED_MEMORY_NAME_AFFIX).append(std::to_wstring((GetProcessId(hProc))));
	hMapFile = CreateFileMappingW(
		INVALID_HANDLE_VALUE,
		nullptr,                
		PAGE_READWRITE,    
		0,                      
		1024,                
		sharedMemoryName.c_str());
	if (!hMapFile)
	{
		std::cout << "cannot create shared memory: " << GetLastError() << std::endl;
		throw std::exception("cannot create shared memory");
	}
	sharedMemoryPtr = MapViewOfFile(hMapFile, FILE_MAP_ALL_ACCESS, 0, 0, 1024);
	if (sharedMemoryPtr)
	{
		std::cout << "create shared memory success" << std::endl;
	}

	// 初始化getOffsets数组!!!, 四个一单位的应该不能用memset
	for (size_t i = 0; i < LENGTH; i++)
	{
		getOffsets()[i] = OFFSET_END;
	}
}

std::optional<void*> SharedMemory::getReadWritePtr() const
{
	int32_t ptr = getOffsets()[0];
	for (size_t i = 1; i < LENGTH; i++)
	{
		if (getOffsets()[i] == OFFSET_END) break;
		ptr = *reinterpret_cast<int32_t*>(ptr);
		if (!ptr) return {};
		ptr += getOffsets()[i];
	}
	if (!ptr || ptr == OFFSET_END) return {}; // 后半个是为了解决[0]==OFFSET_END的问题
	return reinterpret_cast<void*>(ptr);
}

SharedMemory* SharedMemory::getInstance()
{
	if (instancePtr != nullptr) return instancePtr;
	instancePtr = new SharedMemory();
	return instancePtr;
}

bool SharedMemory::deleteInstance()
{
	if (!instancePtr) return false;
	delete instancePtr;
	instancePtr = nullptr;
	return true;
}

bool SharedMemory::readMemory()
{
	*static_cast<volatile uint64_t*>(getReadResult()) = 0;
	bool b = false;
	do
	{
		auto p = getReadWritePtr();
		if (!p.has_value())
		{
			b = false;
			break;
		}
		memcpy(const_cast<void*>(getReadResult()), *p, memoryNum());
		b = true;
	} while (false);
	executeResult() = b ? ExecuteResult::SUCCESS : ExecuteResult::FAIL;
	return b;
}

bool SharedMemory::writeMemory()
{
	bool b = false;
	do {
		auto p = getReadWritePtr();
		if (!p.has_value())
		{
			b = false;
			break;	

		}
		memcpy(p.value(), const_cast<const void*>(getWrittenVal()), memoryNum());
		b = true;
	} while (false);
	executeResult() = b ? ExecuteResult::SUCCESS : ExecuteResult::FAIL;
	return b;
}
