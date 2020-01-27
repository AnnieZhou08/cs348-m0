<?php
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/privacy/dlp/v2/dlp.proto

namespace Google\Cloud\Dlp\V2;

use Google\Protobuf\Internal\GPBType;
use Google\Protobuf\Internal\RepeatedField;
use Google\Protobuf\Internal\GPBUtil;

/**
 * InfoType description.
 *
 * Generated from protobuf message <code>google.privacy.dlp.v2.InfoTypeDescription</code>
 */
class InfoTypeDescription extends \Google\Protobuf\Internal\Message
{
    /**
     * Internal name of the infoType.
     *
     * Generated from protobuf field <code>string name = 1;</code>
     */
    private $name = '';
    /**
     * Human readable form of the infoType name.
     *
     * Generated from protobuf field <code>string display_name = 2;</code>
     */
    private $display_name = '';
    /**
     * Which parts of the API supports this InfoType.
     *
     * Generated from protobuf field <code>repeated .google.privacy.dlp.v2.InfoTypeSupportedBy supported_by = 3;</code>
     */
    private $supported_by;

    public function __construct() {
        \GPBMetadata\Google\Privacy\Dlp\V2\Dlp::initOnce();
        parent::__construct();
    }

    /**
     * Internal name of the infoType.
     *
     * Generated from protobuf field <code>string name = 1;</code>
     * @return string
     */
    public function getName()
    {
        return $this->name;
    }

    /**
     * Internal name of the infoType.
     *
     * Generated from protobuf field <code>string name = 1;</code>
     * @param string $var
     * @return $this
     */
    public function setName($var)
    {
        GPBUtil::checkString($var, True);
        $this->name = $var;

        return $this;
    }

    /**
     * Human readable form of the infoType name.
     *
     * Generated from protobuf field <code>string display_name = 2;</code>
     * @return string
     */
    public function getDisplayName()
    {
        return $this->display_name;
    }

    /**
     * Human readable form of the infoType name.
     *
     * Generated from protobuf field <code>string display_name = 2;</code>
     * @param string $var
     * @return $this
     */
    public function setDisplayName($var)
    {
        GPBUtil::checkString($var, True);
        $this->display_name = $var;

        return $this;
    }

    /**
     * Which parts of the API supports this InfoType.
     *
     * Generated from protobuf field <code>repeated .google.privacy.dlp.v2.InfoTypeSupportedBy supported_by = 3;</code>
     * @return \Google\Protobuf\Internal\RepeatedField
     */
    public function getSupportedBy()
    {
        return $this->supported_by;
    }

    /**
     * Which parts of the API supports this InfoType.
     *
     * Generated from protobuf field <code>repeated .google.privacy.dlp.v2.InfoTypeSupportedBy supported_by = 3;</code>
     * @param int[]|\Google\Protobuf\Internal\RepeatedField $var
     * @return $this
     */
    public function setSupportedBy($var)
    {
        $arr = GPBUtil::checkRepeatedField($var, \Google\Protobuf\Internal\GPBType::ENUM, \Google\Cloud\Dlp\V2\InfoTypeSupportedBy::class);
        $this->supported_by = $arr;

        return $this;
    }

}

