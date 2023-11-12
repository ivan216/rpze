#pragma once
#include "Memory.h"
#include "stdafx.h"
#include <pybind11/stl.h>
// 给Python侧暴露的类型

class Controller
{
	Memory mem;
public:
	explicit Controller(DWORD pid) : mem(pid) {}

	inline DWORD pid() { return mem.getPid(); }

	inline std::optional<int32_t> get_time() const
	{
		auto t = mem.getGameTime();
		if (t == INT32_MIN) return {};
		return t;
	}

	inline std::tuple<bool, uint32_t> get_p_board() const // 第一位返回0表示无须换新
	{
		return mem.getPBoard();
	}

	inline void next_frame() { mem.next(); }

	inline void before() { while (mem.isBlocked()) {} }

	inline bool start_jump_frame() { return mem.startJumpFrame(); }

	inline bool end_jump_frame() { return mem.endJumpFrame(); }

	template <typename T>
	inline std::optional<T> read_memory(const std::vector<int32_t>& offsets) 
	{ return mem.readMemory<T>(offsets); }

	template <typename T>
	inline bool write_memory(T&& val, const std::vector<int32_t>& offsets) 
	{ return mem.writeMemory(val, offsets); }

	inline bool run_code(const char* codes, int num) { return mem.runCode(codes, num); }

	inline void end() { mem.endControl(); }

	inline void start() { mem.getGlobalState() = GlobalState::CONNECTED; }

	inline uint32_t result_address() { return mem.getWrittenAddress(); }

	template<typename T>
	T get_result() { static_assert(sizeof(T) <= 8);  return *static_cast<volatile T*>(mem.getReturnResult()); }

	bool operator==(const Controller& other) const { return mem.getPid() == other.mem.getPid(); }

	bool operator!=(const Controller& other) const { return mem.getPid() != other.mem.getPid(); }

	template<typename T>
	void set_result(T val)
	{
		static_assert(sizeof(T) <= 8);
		*static_cast<volatile T*>(mem.getReturnResult()) = val;
	}
};
