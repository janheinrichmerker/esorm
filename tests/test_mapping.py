from datetime import datetime
from enum import StrEnum
from typing import (
    Annotated,
    Any,
    cast,
)

from esorm.fields import (
    Keyword,
    Text,
    Binary,
    Byte,
    Short,
    Integer,
    Long,
    UnsignedLong,
    HalfFloat,
    Float,
    Double,
    LatLon,
    keyword,
    text,
    binary,
    byte,
    short,
    int32,
    long,
    unsigned_long,
    uint64,
    float16,
    float32,
    double,
    geo_point,
    integer,
    half_float,
    int64,
    boolean,
)
from pydantic import BaseModel, HttpUrl, Field
from pydantic.fields import FieldInfo

from esorm.model import get_field_data, create_mapping


def test_get_field_data() -> None:
    assert get_field_data(
        FieldInfo.from_annotation(
            Keyword,
        )
    ) == {
        "type": "keyword",
    }
    assert get_field_data(
        FieldInfo.from_annotation(
            Text,
        )
    ) == {
        "type": "text",
    }
    assert get_field_data(
        FieldInfo.from_annotation(
            Binary,
        )
    ) == {
        "type": "binary",
    }
    assert get_field_data(
        FieldInfo.from_annotation(
            Byte,
        )
    ) == {
        "type": "byte",
    }
    assert get_field_data(
        FieldInfo.from_annotation(
            Short,
        )
    ) == {
        "type": "short",
    }
    assert get_field_data(
        FieldInfo.from_annotation(
            Integer,
        )
    ) == {
        "type": "integer",
    }
    assert get_field_data(
        FieldInfo.from_annotation(
            Long,
        )
    ) == {
        "type": "long",
    }
    assert get_field_data(
        FieldInfo.from_annotation(
            UnsignedLong,
        )
    ) == {
        "type": "unsigned_long",
    }
    assert get_field_data(
        FieldInfo.from_annotation(
            HalfFloat,
        )
    ) == {"type": "half_float"}
    assert get_field_data(
        FieldInfo.from_annotation(
            Float,
        )
    ) == {
        "type": "float",
    }
    assert get_field_data(
        FieldInfo.from_annotation(
            Double,
        )
    ) == {
        "type": "double",
    }
    assert get_field_data(
        FieldInfo.from_annotation(
            LatLon,
        )
    ) == {
        "type": "geo_point",
    }

    assert get_field_data(
        FieldInfo.from_annotation(
            cast(type[Any], keyword),
        )
    ) == {
        "type": "keyword",
    }
    assert get_field_data(
        FieldInfo.from_annotation(
            cast(type[Any], text),
        )
    ) == {
        "type": "text",
    }
    assert get_field_data(
        FieldInfo.from_annotation(
            cast(type[Any], binary),
        )
    ) == {
        "type": "binary",
    }
    assert get_field_data(
        FieldInfo.from_annotation(
            cast(type[Any], byte),
        )
    ) == {
        "type": "byte",
    }
    assert get_field_data(
        FieldInfo.from_annotation(
            cast(type[Any], short),
        )
    ) == {
        "type": "short",
    }
    assert get_field_data(
        FieldInfo.from_annotation(
            cast(type[Any], int32),
        )
    ) == {
        "type": "integer",
    }
    assert get_field_data(
        FieldInfo.from_annotation(
            cast(type[Any], long),
        )
    ) == {
        "type": "long",
    }
    assert get_field_data(
        FieldInfo.from_annotation(
            cast(type[Any], unsigned_long),
        )
    ) == {
        "type": "unsigned_long",
    }
    assert get_field_data(
        FieldInfo.from_annotation(
            cast(type[Any], uint64),
        )
    ) == {
        "type": "unsigned_long",
    }
    assert get_field_data(
        FieldInfo.from_annotation(
            cast(type[Any], float16),
        )
    ) == {
        "type": "half_float",
    }
    assert get_field_data(
        FieldInfo.from_annotation(
            cast(type[Any], float32),
        )
    ) == {
        "type": "float",
    }
    assert get_field_data(
        FieldInfo.from_annotation(
            cast(type[Any], double),
        )
    ) == {
        "type": "double",
    }
    assert get_field_data(
        FieldInfo.from_annotation(
            geo_point,
        )
    ) == {
        "type": "geo_point",
    }
    assert get_field_data(
        FieldInfo.from_annotation(
            cast(type[Any], integer),
        )
    ) == {
        "type": "integer",
    }
    assert get_field_data(
        FieldInfo.from_annotation(
            cast(type[Any], half_float),
        )
    ) == {
        "type": "half_float",
    }
    assert get_field_data(
        FieldInfo.from_annotation(
            cast(type[Any], int64),
        )
    ) == {
        "type": "long",
    }
    assert get_field_data(
        FieldInfo.from_annotation(
            boolean,
        )
    ) == {
        "type": "boolean",
    }

    assert get_field_data(FieldInfo.from_annotation(str)) == {"type": "keyword"}
    assert get_field_data(FieldInfo.from_annotation(int)) == {"type": "long"}
    assert get_field_data(FieldInfo.from_annotation(float)) == {"type": "double"}
    assert get_field_data(FieldInfo.from_annotation(bool)) == {"type": "boolean"}
    assert get_field_data(FieldInfo.from_annotation(HttpUrl)) == {"type": "keyword"}
    assert get_field_data(
        FieldInfo.merge_field_infos(
            FieldInfo.from_annotation(str),
            FieldInfo.from_field(
                json_schema_extra={
                    "max_length": 100,
                }
            ),
        )
    ) == {
        "type": "keyword",
        "max_length": 100,
    }


def test_create_mapping() -> None:
    class FooEnum(StrEnum):
        bar = "bar"
        baz = "baz"

    class Bar(BaseModel):
        foo: FooEnum

    class Test(BaseModel):
        name: str
        age: integer
        homepage: HttpUrl
        foo: Annotated[
            datetime,
            Field(
                json_schema_extra={
                    "default_timezone": "UTC",
                    "format": "strict_date_time_no_millis",
                }
            ),
        ]
        bar: Bar
        baz: list[int]
        qux: list[Bar]

    mapping = create_mapping(Test)

    assert mapping == {
        "properties": {
            "name": {"type": "keyword"},
            "age": {"type": "integer"},
            "homepage": {"type": "keyword"},
            "foo": {
                "type": "date",
                "format": "strict_date_time_no_millis",
                "default_timezone": "UTC",
            },
            "bar": {
                "type": "object",
                "properties": {
                    "foo": {"type": "keyword"},
                },
            },
            "baz": {"type": "long"},
            "qux": {
                "type": "nested",
                "properties": {
                    "foo": {"type": "keyword"},
                },
            },
        }
    }
